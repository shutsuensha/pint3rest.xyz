from fastapi import APIRouter, HTTPException, Response, status, UploadFile
from .schemas import UserIn, UserOut, PasswordResetRequestModel
from app.api.dependencies import db, user_id
from sqlalchemy import insert, select, update
from app.database.models import UsersOrm
from app.api.utils import hash_password, verify_password, create_access_token, save_file, create_url_safe_token, decode_url_safe_token
import uuid
from fastapi.responses import FileResponse
from app.config import settings
from app.celery.tasks import send_email


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserIn, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.username == user_in.username))
    if user:
        raise HTTPException(status_code=409, detail="user already exists")
    if user_in.email:
        user = await db.scalar(
            insert(UsersOrm)
            .values(username=user_in.username, hashed_password=hash_password(user_in.password), email=user_in.email)
            .returning(UsersOrm)
        )
        await db.commit()

        token = create_url_safe_token({"username": user_in.username})
        link = f"http://{settings.DOMAIN}/users/verify/{token}"

        html_message = f"""
        <h1>Verify your Email</h1>
        <p>Please click this <a href="{link}">link</a> to verify your account {user.username}</p>
        """

        emails = [user_in.email]
        subject = "Verify Your email"
        send_email.delay(emails, subject, html_message)
    else:
        user = await db.scalar(
            insert(UsersOrm)
            .values(username=user_in.username, hashed_password=hash_password(user_in.password))
            .returning(UsersOrm)
        )
        await db.commit()
    return user


@router.get("/verify/{token}", response_model=UserOut)
async def verify_user_account(token: str, db: db):
    token_data = decode_url_safe_token(token)
    user_username = token_data.get("username")

    user = await db.scalar(select(UsersOrm).where(UsersOrm.username == user_username))
    if not user:
        raise HTTPException(status_code=409, detail="user not found")


    user = await db.scalar(
        update(UsersOrm)
        .where(UsersOrm.username == user_username)
        .values(verified = True)
        .returning(UsersOrm)
    )
    await db.commit()

    return user


@router.post("/password-reset-request")
async def password_reset_request(reset_model: PasswordResetRequestModel, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.username == reset_model.username))
    if not user:
        raise HTTPException(status_code=409, detail="user not found")
    if not user.email:
        raise HTTPException(status_code=403, detail="user email not found")
    
    token = create_url_safe_token({"username": user.username, "password": reset_model.password})
    link = f"http://{settings.DOMAIN}/users/password-reset-confirm/{token}"

    html_message = f"""
    <h1>Reset Your Password</h1>
    <p>Please click this <a href="{link}">link</a> to Reset Your Password for account {user.username}</p>
    """
    subject = "Reset Your Password"

    send_email.delay([user.email], subject, html_message)


    return {"message": "password reset link is send to your email"}


@router.get("/password-reset-confirm/{token}")
async def reset_account_password(token: str, db: db):
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

    return {"message": "password updated"}
    

@router.post("/login")
async def login_user(user_in: UserIn, response: Response, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.username == user_in.username))
    if not user:
        raise HTTPException(status_code=401, detail="user not found")
    if not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="password dont match")
    if user.email and not user.verified:
        token = create_url_safe_token({"username": user.username})
        link = f"http://{settings.DOMAIN}/users/verify/{token}"

        html_message = f"""
        <h1>Verify your Email</h1>
        <p>Please click this <a href="{link}">link</a> to verify your account {user.username}</p>
        """

        emails = [user.email]
        subject = "Verify Your email"
        send_email.delay(emails, subject, html_message)

        raise HTTPException(status_code=403 , detail="user not verified, verification link is send to email")
        

    access_token = create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router.get("/me", response_model=UserOut)
async def get_me(user_id: user_id, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id))
    return user


@router.get("/user_id/{id}", response_model=UserOut)
async def get_user_by_id(user_id: user_id, id: int, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user


@router.get("/user_username/{username}", response_model=UserOut)
async def get_user_by_username(user_id: user_id, username: str, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.username == username))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user


@router.post("/upload/{id}", response_model=UserOut)
async def upload_image(id: int, db: db, file: UploadFile):

    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    image_path = f"app/media/users/{unique_filename}"
    save_file(file.file, image_path)
    

    user = await db.scalar(
        update(UsersOrm)
        .where(UsersOrm.id == id)
        .values(image = image_path)
        .returning(UsersOrm)
    )
    await db.commit()

    return user


@router.get("/upload/{id}")
async def get_image(user_id: user_id, id: int, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    
    return FileResponse(user.image)