import json
import uuid
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, Request, Response, UploadFile, status
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy import insert, select, update

from app.api.rest.dependencies import db, user_id
from app.api.rest.utils import (
    create_access_token,
    create_refresh_token,
    create_url_safe_token,
    decode_url_safe_token,
    delete_file,
    encode_token,
    hash_password,
    save_file,
    verify_password,
)
from app.celery.tasks import send_email
from app.config import settings
from app.postgresql.models import UsersOrm
from app.redis.redis_revoke_tokens import is_token_revoked, revoke_token

from .schemas import PasswordResetRequestModel, UserIn, UserOut, UserPatch

router = APIRouter(prefix="/users", tags=["users"])

templates = Jinja2Templates(directory="app/templates")


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "User successfully registered. If an email is provided, a confirmation email is sent.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "username": "example_user",
                        "image": None,
                        "email": "user@example.com",
                        "verified": False,
                        "banner_image": None,
                        "description": None,
                        "instagram": None,
                        "tiktok": None,
                        "telegram": None,
                        "pinterest": None,
                    }
                }
            },
        },
        409: {
            "description": "A user with this username already exists.",
            "content": {"application/json": {"example": {"detail": "user already exists"}}},
        },
    },
)
async def register_user(user_in: UserIn, db: db):
    """
    Registers a new user.

    - **username**: unique username
    - **password**: user's password (will be hashed)
    - **email** (optional): if provided, a confirmation email will be sent
    - **Response**: user object without the password
    """
    user = await db.scalar(select(UsersOrm).where(UsersOrm.username == user_in.username))
    if user:
        raise HTTPException(status_code=409, detail="user already exists")
    if user_in.email:
        user = await db.scalar(
            insert(UsersOrm)
            .values(
                username=user_in.username,
                hashed_password=hash_password(user_in.password),
                email=user_in.email,
            )
            .returning(UsersOrm)
        )
        await db.commit()

        token = create_url_safe_token({"username": user_in.username})
        link = f"{settings.API_DOMAIN}/users/verify/{token}"

        context = {"username": user.username, "link": link}

        emails = [user_in.email]
        subject = "Verify Your email"
        send_email.delay(emails, subject, context, "mail_verification.html")
    else:
        user = await db.scalar(
            insert(UsersOrm)
            .values(
                username=user_in.username,
                hashed_password=hash_password(user_in.password),
            )
            .returning(UsersOrm)
        )
        await db.commit()
    return user


@router.get(
    "/verify/{token}",
    response_class=HTMLResponse,
    responses={
        200: {
            "description": "User account successfully confirmed",
            "content": {
                "text/html": {
                    "example": "<html><body><h1>Account successfully confirmed</h1></body></html>"
                }
            },
        },
        409: {
            "description": "User not found",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        },
    },
)
async def verify_user_account(request: Request, token: str, db: db):
    """
    Confirms the user's account with the provided token.

    - **token**: The token used for confirming the user, which contains the username.
    - Returns a page with a successful confirmation if the user is found and successfully confirmed.
    - Returns a 409 error if the user is not found.

    **Responses:**
    - 200: Successful account confirmation.
    """
    token_data = decode_url_safe_token(token)
    user_username = token_data.get("username")

    user = await db.scalar(select(UsersOrm).where(UsersOrm.username == user_username))
    if not user:
        raise HTTPException(status_code=409, detail="user not found")

    user = await db.scalar(
        update(UsersOrm)
        .where(UsersOrm.username == user_username)
        .values(verified=True)
        .returning(UsersOrm)
    )
    await db.commit()

    return templates.TemplateResponse(
        request=request,
        name="success_verification.html",
        context={"user": user, "home_link": f"{settings.FRONTEND_DOMAIN}"},
    )


@router.post(
    "/password-reset-request",
    responses={
        200: {
            "description": "Password reset link has been successfully sent to your email",
            "content": {
                "application/json": {
                    "example": {"message": "password reset link is sent to your email"}
                }
            },
        },
        404: {
            "description": "User not found",
            "content": {"application/json": {"example": {"detail": "user not found"}}},
        },
        403: {
            "description": "User does not have an email associated for password reset",
            "content": {
                "application/json": {
                    "example": {"detail": "user does not have email, you can't reset password"}
                }
            },
        },
        400: {
            "description": "Invalid email for password reset",
            "content": {
                "application/json": {
                    "example": {"detail": "enter your email for account <username>"}
                }
            },
        },
        405: {
            "description": "Error while resetting password, email confirmation required",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "first you need to verify your email, then you can reset password, verification link is sent to your email"
                    }
                }
            },
        },
    },
)
async def password_reset_request(reset_model: PasswordResetRequestModel, db: db):
    """
    Request to reset the user's password.

    - **reset_model.username**: The username for which the password reset is requested.
    - **reset_model.email**: The email provided by the user for password reset.
    - **reset_model.password**: The new password to be set after the reset.

    **Responses:**
    - 200: Password reset link has been successfully sent to the email.
    - 404: User not found.
    - 403: User does not have an email for password reset.
    - 400: Invalid email entered for the specified user.
    - 405: Error resetting password, email confirmation required.
    """
    user = await db.scalar(select(UsersOrm).where(UsersOrm.username == reset_model.username))
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    if not user.email:
        raise HTTPException(
            status_code=403,
            detail=f"{reset_model.username} does not have email, u cant do password reset :(",
        )
    if reset_model.email != user.email:
        raise HTTPException(status_code=400, detail=f"enter your email for account {user.username}")
    if not user.verified:
        token = create_url_safe_token({"username": user.username})
        link = f"{settings.API_DOMAIN}/users/verify/{token}"

        context = {"username": user.username, "link": link}

        emails = [user.email]
        subject = "Verify Your email"
        send_email.delay(emails, subject, context, "mail_verification.html")
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="first u need verify your email then u can password, verification link is send to your email",
        )
    if user.google_id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="HTTP_406_NOT_ACCEPTABLE "
        )

    token = create_url_safe_token({"username": user.username, "password": reset_model.password})
    link = f"{settings.API_DOMAIN}/users/password-reset-confirm/{token}"

    subject = "Reset Your Password"

    context = {
        "username": user.username,
        "link": link,
        "new_password": reset_model.password,
    }

    send_email.delay([user.email], subject, context, "mail_password_reset.html")

    return {"message": "password reset link is send to your email"}


@router.get(
    "/password-reset-confirm/{token}",
    response_class=HTMLResponse,
    responses={
        200: {
            "description": "Password successfully reset",
            "content": {
                "text/html": {
                    "example": "<html><body><h1>Password successfully reset</h1></body></html>"
                }
            },
        },
        409: {
            "description": "User not found",
            "content": {"application/json": {"example": {"detail": "user not found"}}},
        },
        400: {
            "description": "Invalid token for password reset",
            "content": {
                "application/json": {"example": {"detail": "Invalid token for password reset"}}
            },
        },
    },
)
async def reset_account_password(request: Request, token: str, db: db):
    """
    Reset the user's password using a token.

    - **token**: The token containing the username and the new password.
    - Returns a page with a successful password reset if all data is correct.
    - Returns error 409 if the user is not found.
    - Returns error 400 if the password reset token is invalid.

    **Responses:**
    - 200: Password successfully reset.
    - 409: User not found.
    - 400: Invalid token for password reset.
    """
    token_data = decode_url_safe_token(token)

    username = token_data.get("username")
    password = token_data.get("password")

    user = await db.scalar(select(UsersOrm).where(UsersOrm.username == username))
    if not user:
        raise HTTPException(status_code=409, detail="user not found")

    await db.execute(
        update(UsersOrm)
        .where(UsersOrm.username == username)
        .values(hashed_password=hash_password(password))
    )
    await db.commit()

    return templates.TemplateResponse(
        request=request,
        name="success_password_reset.html",
        context={"user": user, "home_link": f"{settings.FRONTEND_DOMAIN}"},
    )


@router.post(
    "/login",
    responses={
        200: {
            "description": "User successfully logged in",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "<access_token>",
                        "refresh_token": "<refresh_token>",
                    }
                }
            },
        },
        401: {
            "description": "Invalid login credentials",
            "content": {"application/json": {"example": {"detail": "user not found"}}},
        },
        403: {
            "description": "User has not verified their email",
            "content": {
                "application/json": {"example": {"detail": "Verification link is sent to <email>"}}
            },
        },
    },
)
async def login_user(user_in: UserIn, response: Response, db: db):
    """
    User login.

    - **user_in.username**: Username for login.
    - **user_in.password**: Password for login.

    **Responses:**
    - 200: User successfully logged in, returns tokens.
    - 401: Invalid login credentials (user not found or incorrect password).
    - 403: User has not verified their email, a verification link has been sent to their email.
    """
    user = await db.scalar(select(UsersOrm).where(UsersOrm.username == user_in.username))
    if not user:
        raise HTTPException(status_code=401, detail="user not found")
    if not user_in.password or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="password dont match")
    if user.email and not user.verified:
        token = create_url_safe_token({"username": user_in.username})
        link = f"{settings.API_DOMAIN}/users/verify/{token}"

        context = {"username": user.username, "link": link}

        emails = [user.email]
        subject = "Verify Your email"
        send_email.delay(emails, subject, context, "mail_verification.html")

        raise HTTPException(status_code=403, detail=f"Verification link is send to {user.email}")

    access_token = create_access_token({"user_id": user.id})
    refresh_token = create_refresh_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    response.set_cookie("refresh_token", refresh_token)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.get(
    "/refresh_token",
    responses={
        200: {
            "description": "New access token successfully issued",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "<access_token>",
                        "refresh_token": "<refresh_token>",
                    }
                }
            },
        },
        401: {
            "description": "Authorization error, token not provided or has been revoked",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
    },
)
async def get_new_access_token(request: Request, response: Response):
    """
    Get a new access token using the refresh token.

    - **refresh_token**: The refresh token that should be passed in the cookies.

    **Responses:**
    - 200: A new access token is issued, returns both access and refresh tokens.
    - 401: Authorization error, refresh token not provided or has been revoked.
    """
    refresh_token = request.cookies.get("refresh_token", None)
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if await is_token_revoked(refresh_token):
        raise HTTPException(status_code=401, detail="Token is revoked")
    data = encode_token(refresh_token)
    access_token = create_access_token({"user_id": data["user_id"]})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post(
    "/logout",
    responses={
        200: {
            "description": "User successfully logged out",
            "content": {"application/json": {"example": {"status": "OK"}}},
        }
    },
)
async def logout(response: Response, request: Request):
    """
    User logout.

    Removes the access and refresh tokens from cookies and revokes them.

    **Responses:**
    - 200: User successfully logged out.
    """
    access_token = request.cookies.get("access_token", None)
    refresh_token = request.cookies.get("refresh_token", None)

    if access_token:
        await revoke_token(access_token, settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        response.delete_cookie("access_token")
    if refresh_token:
        await revoke_token(refresh_token, settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        response.delete_cookie("refresh_token")

    return {"status": "OK"}


@router.get(
    "/me",
    response_model=UserOut,
    responses={
        200: {
            "description": "User found and returned",
            "content": {
                "application/json": {
                    "example": {"id": 1, "username": "username", "image": "image.jpg"}
                }
            },
        }
    },
)
async def get_me(user_id: user_id, db: db):
    """
    Get information about the current user by ID.

    - **user_id**: The user ID to retrieve their data.

    **Responses:**
    - 200: User information successfully returned.
    """
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id))
    return user


@router.get(
    "/user_id/{id}",
    response_model=UserOut,
    responses={
        200: {
            "description": "User found and returned",
            "content": {
                "application/json": {
                    "example": {"id": 1, "username": "username", "image": "image.jpg"}
                }
            },
        },
        404: {
            "description": "User not found",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        },
    },
)
async def get_user_by_id(user_id: user_id, id: int, db: db):
    """
    Retrieve user information by ID.

    - **id**: The user's ID to retrieve their data.

    **Responses:**
    - 200: User information successfully returned.
    - 404: User not found.
    """
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user


@router.get(
    "/user_username/{username}",
    response_model=UserOut,
    responses={
        200: {
            "description": "User found and returned",
            "content": {
                "application/json": {
                    "example": {"id": 1, "username": "username", "image": "image.jpg"}
                }
            },
        },
        404: {
            "description": "User not found",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        },
    },
)
async def get_user_by_username(user_id: user_id, username: str, db: db):
    """
    Get user information by username.

    - **username**: The username to retrieve the user's data.

    **Responses:**
    - 200: User information successfully returned.
    - 404: User not found.
    """
    user = await db.scalar(select(UsersOrm).where(UsersOrm.username == username))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user


@router.post(
    "/upload/{id}",
    response_model=UserOut,
    responses={
        200: {
            "description": "Image successfully uploaded and updated",
            "content": {
                "application/json": {
                    "example": {"id": 1, "username": "username", "image": "image_path"}
                }
            },
        },
        404: {
            "description": "User not found",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        },
    },
)
async def upload_image(id: int, db: db, file: UploadFile):
    """
    Image upload for the user.

    - **id**: User ID for which the image is being uploaded.
    - **file**: The uploaded image file.

    **Responses:**
    - 200: Image successfully uploaded and updated.
    - 404: User not found.
    """

    ALLOWED_FILE_TYPES = [
        "image/jpeg",
        "image/jpg",
        "image/gif",
        "image/webp",
        "image/png",
        "image/bmp",
    ]

    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=415,
            detail="Invalid file type. Allowed types: .jpg, .jpeg, .gif, .webp, .png, .bmp",
        )

    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    image_path = f"{settings.MEDIA_PATH}users/{unique_filename}"

    await save_file(file.file, image_path)
    if user.image:
        await delete_file(user.image)

    user = await db.scalar(
        update(UsersOrm).where(UsersOrm.id == id).values(image=image_path).returning(UsersOrm)
    )
    await db.commit()

    return user


@router.get(
    "/upload/{id}",
    responses={
        200: {
            "description": "User's image successfully found and returned",
            "content": {"application/octet-stream": {}},
        },
        404: {
            "description": "User not found",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        },
    },
)
async def get_image(user_id: user_id, id: int, db: db):
    """
    Get the user's image by ID.

    - **id**: The ID of the user whose image is to be retrieved.

    **Responses:**
    - 200: The user's image was found and returned.
    - 404: User not found.
    """
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    return FileResponse(user.image)


@router.post(
    "/banner/upload/{id}",
    response_model=UserOut,
    responses={
        200: {
            "description": "The banner image was successfully uploaded and updated.",
            "content": {
                "application/json": {
                    "example": {"id": 1, "username": "user1", "banner_image": "path/to/banner.jpg"}
                }
            },
        }
    },
)
async def update_user_banner_image(id: int, db: db, file: UploadFile):
    """
    Updating the user's banner image by ID.

    - **id**: The ID of the user whose banner needs to be updated.
    - **file**: The new banner image file.

    **Responses:**
    - 200: The banner image was successfully updated.
    """

    ALLOWED_FILE_TYPES = [
        "image/jpeg",
        "image/jpg",
        "image/gif",
        "image/webp",
        "image/png",
        "image/bmp",
    ]

    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=415,
            detail="Invalid file type. Allowed types: .jpg, .jpeg, .gif, .webp, .png, .bmp",
        )

    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))

    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    image_path = f"{settings.MEDIA_PATH}users/{unique_filename}"
    await save_file(file.file, image_path)
    if user.banner_image:
        await delete_file(user.banner_image)

    user = await db.scalar(
        update(UsersOrm)
        .where(UsersOrm.id == id)
        .values(banner_image=image_path)
        .returning(UsersOrm)
    )
    await db.commit()

    return user


@router.get(
    "/banner/upload/{id}",
    responses={
        200: {
            "description": "The user's banner image was successfully found and returned.",
            "content": {"application/octet-stream": {}},
        },
        404: {
            "description": "User not found",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        },
    },
)
async def get_user_banner(user_id: user_id, id: int, db: db):
    """
    Get the user's banner image by ID.

    - **id**: The user's ID whose banner image needs to be fetched.

    **Responses:**
    - 200: The banner image was found and returned.
    - 404: User not found.
    """
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    return FileResponse(user.banner_image)


@router.patch(
    "/information",
    response_model=UserOut,
    responses={
        200: {
            "description": "User information successfully updated.",
            "content": {"application/json": {"example": {"id": 1, "username": "new_username"}}},
        },
        409: {
            "description": "User not found.",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        },
    },
)
async def update_user_information(user_model: UserPatch, user_id: user_id, db: db):
    """
    Update user information (e.g., username, description, etc.).

    - **user_id**: The ID of the user whose information needs to be updated.
    - **user_model**: The data model for updating the user's information.

    **Responses:**
    - 200: User information successfully updated.
    - 409: User with this ID not found.
    """
    if user_model.username:
        user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id))
        if user.username == 'testusername':
            raise HTTPException(status_code=403, detail="u cannot change username of test account")

        user = await db.scalar(select(UsersOrm).where(UsersOrm.username == user_model.username))
        if user:
            raise HTTPException(status_code=409, detail="user already exists")
    user = await db.scalar(
        update(UsersOrm)
        .values(**user_model.model_dump(exclude_none=True))
        .where(UsersOrm.id == user_id)
        .returning(UsersOrm)
    )
    await db.commit()
    return user


@router.post("/create-user-entity", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user_entity(db: db, user_model: str = Form(...), file: UploadFile = File(...)):
    ALLOWED_FILE_TYPES = [
        "image/jpeg",
        "image/jpg",
        "image/gif",
        "image/webp",
        "image/png",
        "image/bmp",
    ]

    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=415,
            detail="Invalid file type. Allowed types: .jpg, .jpeg, .gif, .webp, .png, .bmp",
        )

    try:
        user_in = json.loads(user_model)
        user_in = UserIn(**user_in)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {e.errors()}")

    user = await db.scalar(select(UsersOrm).where(UsersOrm.username == user_in.username))
    if user:
        raise HTTPException(status_code=409, detail="user already exists")
    if user_in.email:
        user = await db.scalar(
            insert(UsersOrm)
            .values(
                username=user_in.username,
                hashed_password=hash_password(user_in.password),
                email=user_in.email,
            )
            .returning(UsersOrm)
        )
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        image_path = f"{settings.MEDIA_PATH}users/{unique_filename}"

        await save_file(file.file, image_path)
        if user.image:
            await delete_file(user.image)

        user = await db.scalar(
            update(UsersOrm)
            .where(UsersOrm.id == user.id)
            .values(image=image_path)
            .returning(UsersOrm)
        )

        token = create_url_safe_token({"username": user_in.username})
        link = f"{settings.API_DOMAIN}/users/verify/{token}"

        context = {"username": user.username, "link": link}

        emails = [user_in.email]
        subject = "Verify Your email"
        send_email.delay(emails, subject, context, "mail_verification.html")
    else:
        user = await db.scalar(
            insert(UsersOrm)
            .values(
                username=user_in.username,
                hashed_password=hash_password(user_in.password),
            )
            .returning(UsersOrm)
        )

        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        image_path = f"{settings.MEDIA_PATH}users/{unique_filename}"

        await save_file(file.file, image_path)
        if user.image:
            await delete_file(user.image)

        user = await db.scalar(
            update(UsersOrm)
            .where(UsersOrm.id == user.id)
            .values(image=image_path)
            .returning(UsersOrm)
        )

    await db.commit()
    return user
