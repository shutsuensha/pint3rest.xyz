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
            "description": "Пользователь успешно зарегистрирован. Если указан email, отправляется письмо с подтверждением.",
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
            "description": "Пользователь с таким именем уже существует.",
            "content": {"application/json": {"example": {"detail": "user already exists"}}},
        },
    },
)
async def register_user(user_in: UserIn, db: db):
    """
    Регистрирует нового пользователя.

    - **username**: уникальное имя пользователя
    - **password**: пароль пользователя (будет захеширован)
    - **email** (необязательно): если указан, отправляется письмо с подтверждением
    - **Ответ**: объект пользователя без пароля
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
            "description": "Учетная запись пользователя успешно подтверждена",
            "content": {
                "text/html": {
                    "example": "<html><body><h1>Аккаунт успешно подтвержден</h1></body></html>"
                }
            },
        },
        409: {
            "description": "Пользователь не найден",
            "content": {"application/json": {"example": {"detail": "Пользователь не найден"}}},
        },
    },
)
async def verify_user_account(request: Request, token: str, db: db):
    """
    Подтверждает учетную запись пользователя по предоставленному токену.

    - **token**: Токен, используемый для подтверждения пользователя, содержащий имя пользователя.
    - Возвращает страницу с успешным подтверждением, если пользователь найден и успешно подтвержден.
    - Возвращает ошибку 409, если пользователь не найден.

    **Ответы:**
    - 200: Успешное подтверждение учетной записи.
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
            "description": "Ссылка для сброса пароля успешно отправлена на вашу почту",
            "content": {
                "application/json": {
                    "example": {"message": "password reset link is send to your email"}
                }
            },
        },
        404: {
            "description": "Пользователь не найден",
            "content": {"application/json": {"example": {"detail": "user not found"}}},
        },
        403: {
            "description": "Пользователь не имеет привязанного email для сброса пароля",
            "content": {
                "application/json": {
                    "example": {"detail": "user does not have email, u cant do password reset"}
                }
            },
        },
        400: {
            "description": "Неверный email для сброса пароля",
            "content": {
                "application/json": {
                    "example": {"detail": "enter your email for account <username>"}
                }
            },
        },
        405: {
            "description": "Ошибка при сбросе пароля, требуется подтверждение email",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "first u need verify your email then u can password, verification link is send to your email"
                    }
                }
            },
        },
    },
)
async def password_reset_request(reset_model: PasswordResetRequestModel, db: db):
    """
    Запрос на сброс пароля пользователя.

    - **reset_model.username**: Имя пользователя, для которого запрашивается сброс пароля.
    - **reset_model.email**: Email, указанный пользователем для сброса пароля.
    - **reset_model.password**: Новый пароль, который будет установлен после сброса.

    **Ответы:**
    - 200: Ссылка для сброса пароля успешно отправлена на почту.
    - 404: Пользователь не найден.
    - 403: Пользователь не имеет email для сброса пароля.
    - 400: Введен неверный email для указанного пользователя.
    - 405: Ошибка сброса пароля, требуется подтверждение email.
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
            "description": "Пароль успешно сброшен",
            "content": {
                "text/html": {
                    "example": "<html><body><h1>Пароль успешно сброшен</h1></body></html>"
                }
            },
        },
        409: {
            "description": "Пользователь не найден",
            "content": {"application/json": {"example": {"detail": "user not found"}}},
        },
        400: {
            "description": "Неверный токен для сброса пароля",
            "content": {
                "application/json": {"example": {"detail": "Invalid token for password reset"}}
            },
        },
    },
)
async def reset_account_password(request: Request, token: str, db: db):
    """
    Сброс пароля пользователя с помощью токена.

    - **token**: Токен, содержащий имя пользователя и новый пароль.
    - Возвращает страницу с успешным сбросом пароля, если все данные верны.
    - Возвращает ошибку 409, если пользователь не найден.
    - Возвращает ошибку 400, если токен сброса пароля недействителен.

    **Ответы:**
    - 200: Пароль успешно сброшен.
    - 409: Пользователь не найден.
    - 400: Неверный токен для сброса пароля.
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
            "description": "Пользователь успешно вошел в систему",
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
            "description": "Неверные данные для входа",
            "content": {"application/json": {"example": {"detail": "user not found"}}},
        },
        403: {
            "description": "Пользователь не подтвердил email",
            "content": {
                "application/json": {"example": {"detail": "Verification link is send to <email>"}}
            },
        },
    },
)
async def login_user(user_in: UserIn, response: Response, db: db):
    """
    Вход пользователя в систему.

    - **user_in.username**: Имя пользователя для входа.
    - **user_in.password**: Пароль пользователя для входа.

    **Ответы:**
    - 200: Пользователь успешно вошел в систему, возвращает токены.
    - 401: Неверные данные для входа (пользователь не найден или пароль не совпадает).
    - 403: Пользователь не подтвердил email, ссылка на подтверждение отправлена на его почту.
    """
    user = await db.scalar(select(UsersOrm).where(UsersOrm.username == user_in.username))
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
            "description": "Новый access токен успешно выдан",
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
            "description": "Ошибка авторизации, токен не предоставлен или был отозван",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
    },
)
async def get_new_access_token(request: Request, response: Response):
    """
    Получение нового access токена с использованием refresh токена.

    - **refresh_token**: Refresh токен, который должен быть передан в cookies.

    **Ответы:**
    - 200: Новый access токен выдан, возвращает access и refresh токены.
    - 401: Ошибка авторизации, refresh токен не предоставлен или был отозван.
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
            "description": "Пользователь успешно вышел из системы",
            "content": {"application/json": {"example": {"status": "OK"}}},
        }
    },
)
async def logout(response: Response, request: Request):
    """
    Выход пользователя из системы.

    Удаляет access и refresh токены из cookies и отзывает их.

    **Ответы:**
    - 200: Пользователь успешно вышел из системы.
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
            "description": "Пользователь найден и возвращен",
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
    Получение информации о текущем пользователе по ID.

    - **user_id**: ID пользователя для получения его данных.

    **Ответы:**
    - 200: Информация о пользователе успешно возвращена.
    """
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id))
    return user


@router.get(
    "/user_id/{id}",
    response_model=UserOut,
    responses={
        200: {
            "description": "Пользователь найден и возвращен",
            "content": {
                "application/json": {
                    "example": {"id": 1, "username": "username", "image": "image.jpg"}
                }
            },
        },
        404: {
            "description": "Пользователь не найден",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        },
    },
)
async def get_user_by_id(user_id: user_id, id: int, db: db):
    """
    Получение информации о пользователе по ID.

    - **id**: ID пользователя для получения его данных.

    **Ответы:**
    - 200: Информация о пользователе успешно возвращена.
    - 404: Пользователь не найден.
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
            "description": "Пользователь найден и возвращен",
            "content": {
                "application/json": {
                    "example": {"id": 1, "username": "username", "image": "image.jpg"}
                }
            },
        },
        404: {
            "description": "Пользователь не найден",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        },
    },
)
async def get_user_by_username(user_id: user_id, username: str, db: db):
    """
    Получение информации о пользователе по имени пользователя (username).

    - **username**: Имя пользователя для получения его данных.

    **Ответы:**
    - 200: Информация о пользователе успешно возвращена.
    - 404: Пользователь не найден.
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
            "description": "Изображение успешно загружено и обновлено",
            "content": {
                "application/json": {
                    "example": {"id": 1, "username": "username", "image": "image_path"}
                }
            },
        },
        404: {
            "description": "Пользователь не найден",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        },
    },
)
async def upload_image(id: int, db: db, file: UploadFile):
    """
    Загрузка изображения для пользователя.

    - **id**: ID пользователя, для которого загружается изображение.
    - **file**: Загружаемый файл изображения.

    **Ответы:**
    - 200: Изображение успешно загружено и обновлено.
    - 404: Пользователь не найден.
    """

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
            "description": "Изображение пользователя успешно найдено и возвращено",
            "content": {"application/octet-stream": {}},
        },
        404: {
            "description": "Пользователь не найден",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        },
    },
)
async def get_image(user_id: user_id, id: int, db: db):
    """
    Получение изображения пользователя по ID.

    - **id**: ID пользователя, чье изображение нужно получить.

    **Ответы:**
    - 200: Изображение пользователя найдено и возвращено.
    - 404: Пользователь не найден.
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
            "description": "Изображение баннера успешно загружено и обновлено.",
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
    Обновление изображения баннера пользователя по ID.

    - **id**: ID пользователя, чей баннер необходимо обновить.
    - **file**: Новый файл изображения баннера.

    **Ответы:**
    - 200: Изображение баннера успешно обновлено.
    """
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
            "description": "Изображение баннера пользователя успешно найдено и возвращено.",
            "content": {"application/octet-stream": {}},
        },
        404: {
            "description": "Пользователь не найден",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        },
    },
)
async def get_user_banner(user_id: user_id, id: int, db: db):
    """
    Получение изображения баннера пользователя по ID.

    - **id**: ID пользователя, чей баннер нужно получить.

    **Ответы:**
    - 200: Изображение баннера найдено и возвращено.
    - 404: Пользователь не найден.
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
            "description": "Информация пользователя успешно обновлена.",
            "content": {"application/json": {"example": {"id": 1, "username": "new_username"}}},
        },
        409: {
            "description": "Пользователь не найден.",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        },
    },
)
async def update_user_information(user_model: UserPatch, user_id: user_id, db: db):
    """
    Обновление информации пользователя (например, имени пользователя, описания и т. д.).

    - **user_id**: ID пользователя, чью информацию нужно обновить.
    - **user_model**: Модель данных для обновления информации пользователя.

    **Ответы:**
    - 200: Информация пользователя успешно обновлена.
    - 409: Пользователь с таким ID не найден.
    """
    if user_model.username:
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
