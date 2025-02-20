from fastapi import APIRouter, HTTPException, Response, status, UploadFile, Request
from .schemas import UserIn, UserOut, PasswordResetRequestModel, UserPatch
from app.api.rest.dependencies import db, user_id
from sqlalchemy import insert, select, update
from app.database.models import UsersOrm
from app.api.rest.utils import (
    encode_token,
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    save_file,
    create_url_safe_token,
    decode_url_safe_token,
    delete_file,
)
import uuid
from fastapi.responses import FileResponse
from app.config import settings
from app.celery.tasks import send_email
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.redis.redis_revoke_tokens import revoke_token, is_token_revoked
from app.celery.tasks import save_file_celery_and_crop_300x300
from pathlib import Path
from celery.result import AsyncResult
from app.celery.celery_app import celery_instance


router = APIRouter(prefix="/users", tags=["users"])

templates = Jinja2Templates(directory="app/templates")


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserIn, db: db):
    user = await db.scalar(
        select(UsersOrm).where(UsersOrm.username == user_in.username)
    )
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


@router.get("/verify/{token}", response_class=HTMLResponse)
async def verify_user_account(request: Request, token: str, db: db):
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


@router.post("/password-reset-request")
async def password_reset_request(reset_model: PasswordResetRequestModel, db: db):
    user = await db.scalar(
        select(UsersOrm).where(UsersOrm.username == reset_model.username)
    )
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    if not user.email:
        raise HTTPException(
            status_code=403,
            detail=f"{reset_model.username} does not have email, u cant do password reset :(",
        )
    if reset_model.email != user.email:
        raise HTTPException(
            status_code=400, detail=f"enter your email for account {user.username}"
        )
    if not user.verified:

        token = create_url_safe_token({"username": user.username})
        link = f"{settings.API_DOMAIN}/users/verify/{token}"

        context = {"username": user.username, "link": link}

        emails = [user.email]
        subject = "Verify Your email"
        send_email.delay(emails, subject, context, "mail_verification.html")
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"first u need verify your email then u can password, verification link is send to your email",
        )

    token = create_url_safe_token(
        {"username": user.username, "password": reset_model.password}
    )
    link = f"{settings.API_DOMAIN}/users/password-reset-confirm/{token}"

    subject = "Reset Your Password"

    context = {
        "username": user.username,
        "link": link,
        "new_password": reset_model.password,
    }

    send_email.delay([user.email], subject, context, "mail_password_reset.html")

    return {"message": "password reset link is send to your email"}


@router.get("/password-reset-confirm/{token}", response_class=HTMLResponse)
async def reset_account_password(request: Request, token: str, db: db):
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


@router.post("/login")
async def login_user(user_in: UserIn, response: Response, db: db):
    user = await db.scalar(
        select(UsersOrm).where(UsersOrm.username == user_in.username)
    )
    if not user:
        raise HTTPException(status_code=401, detail="user not found")
    if not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="password dont match")
    if user.email and not user.verified:
        token = create_url_safe_token({"username": user_in.username})
        link = f"{settings.API_DOMAIN}/users/verify/{token}"

        context = {"username": user.username, "link": link}

        emails = [user.email]
        subject = "Verify Your email"
        send_email.delay(emails, subject, context, "mail_verification.html")

        raise HTTPException(
            status_code=403, detail=f"Verification link is send to {user.email}"
        )

    access_token = create_access_token({"user_id": user.id})
    refresh_token = create_refresh_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    response.set_cookie("refresh_token", refresh_token)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.get("/refresh_token")
async def get_new_access_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token", None)
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if await is_token_revoked(refresh_token):
        raise HTTPException(status_code=401, detail="Token is revoked")
    data = encode_token(refresh_token)
    access_token = create_access_token({"user_id": data["user_id"]})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/logout")
async def logout(response: Response, request: Request):
    access_token = request.cookies.get("access_token", None)
    refresh_token = request.cookies.get("refresh_token", None)

    if access_token:
        await revoke_token(access_token, settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        response.delete_cookie("access_token")
    if refresh_token:
        await revoke_token(refresh_token, settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        response.delete_cookie("refresh_token")

    return {"status": "OK"}


@router.get("/me", response_model=UserOut)
async def get_me(user_id: user_id, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id))
    return user


@router.get("/user_id/{id}", response_model=UserOut)
async def get_user_by_id(user_id: user_id, id: int, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    return user


@router.get("/user_username/{username}", response_model=UserOut)
async def get_user_by_username(user_id: user_id, username: str, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.username == username))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    return user


@router.post("/upload/celery/{id}")
async def upload_image_celery(id: int, db: db, file: UploadFile):

    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )

    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    image_path = f"app/media/users/{unique_filename}"

    task = save_file_celery_and_crop_300x300.delay(file.file.read(), image_path, id)

    return {"message": "File upload is in progress", "task_id": task.id}


@router.get("/upload/celery/status/{task_id}")
async def get_upload_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_instance)

    if task_result.state == "PENDING":
        return {"status": "pending", "message": "Task is waiting in queue"}
    elif task_result.state == "STARTED":
        return {"status": "processing", "message": "Task is in progress"}
    elif task_result.state == "SUCCESS":
        return {
            "status": "completed",
            "message": "File uploaded successfully",
            "result": task_result.result,
        }
    elif task_result.state == "FAILURE":
        return {"status": "failed", "message": str(task_result.info)}
    else:
        return {"status": task_result.state, "message": "Unknown state"}


@router.post("/upload/{id}", response_model=UserOut)
async def upload_image(id: int, db: db, file: UploadFile):

    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )

    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    image_path = f"app/media/users/{unique_filename}"

    save_file(file.file, image_path)

    user = await db.scalar(
        update(UsersOrm)
        .where(UsersOrm.id == id)
        .values(image=image_path)
        .returning(UsersOrm)
    )
    await db.commit()

    return user


@router.get("/upload/banner/{id}")
async def get_user_banner(id: int, user_id: user_id, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )

    return FileResponse(user.banner_image)


@router.get("/upload/{id}")
async def get_image(user_id: user_id, id: int, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )

    return FileResponse(user.image)


@router.patch("/information", response_model=UserOut)
async def update_user_information(user_model: UserPatch, user_id: user_id, db: db):
    if user_model.username:
        user = await db.scalar(
            select(UsersOrm).where(UsersOrm.username == user_model.username)
        )
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


@router.patch("/upload/profile", response_model=UserOut)
async def update_user_profile_image(user_id: user_id, db: db, file: UploadFile):

    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id))

    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    image_path = f"app/media/users/{unique_filename}"
    save_file(file.file, image_path)
    delete_file(user.image)

    user = await db.scalar(
        update(UsersOrm)
        .where(UsersOrm.id == user_id)
        .values(image=image_path)
        .returning(UsersOrm)
    )
    await db.commit()

    return user


@router.patch("/upload/banner", response_model=UserOut)
async def update_user_banner_image(user_id: user_id, db: db, file: UploadFile):

    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id))

    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    image_path = f"app/media/users/{unique_filename}"
    save_file(file.file, image_path)
    if user.banner_image:
        delete_file(user.banner_image)

    user = await db.scalar(
        update(UsersOrm)
        .where(UsersOrm.id == user_id)
        .values(banner_image=image_path)
        .returning(UsersOrm)
    )
    await db.commit()

    return user
