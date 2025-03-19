from fastapi import APIRouter, Response
from fastapi.responses import RedirectResponse
from app.api.rest.dependencies import db
from app.config import settings
from app.httpx.app import get_httpx_client
from sqlalchemy import select, insert, update
import uuid
from pathlib import Path
from app.api.rest.utils import save_file_bytes, create_access_token, create_refresh_token

from app.postgresql.models import UsersOrm


router = APIRouter(prefix="/users/google/auth", tags=["users-google-auth"])


@router.get("/login/")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.GOOGLE_OAUTH2_CLIENT_ID}&redirect_uri={settings.GOOGLE_OAUTH2_REDIRECT_URI}&scope=openid%20profile%20email&=offline"
    }


@router.get("/")
async def auth_google(code: str, db: db):
    client = get_httpx_client()

    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
        "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_OAUTH2_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = await client.post(token_url, data=data)
    access_token = response.json().get("access_token")

    user_info = await client.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    user_data = user_info.json()
    
    user_by_google_id = await db.scalar(select(UsersOrm).where(UsersOrm.google_id == user_data["id"]))

    if not user_by_google_id:
        username = user_data["email"].split('@')[0]
        user_by_username = await db.scalar(select(UsersOrm).where(UsersOrm.username == username))
        if user_by_username:
            username = f"{username}_{uuid.uuid4().hex[:6]}"
        

        response = await client.get(user_data["picture"])

        unique_filename = f"{uuid.uuid4()}.jpg"
        image_path = f"{settings.MEDIA_PATH}users/{unique_filename}"

        await save_file_bytes(response.content, image_path)


        user_by_google_id = await db.scalar(
            insert(UsersOrm)
            .values(
                google_id=user_data["id"],
                username=username,
                email=user_data["email"],
                verified=True,
                image=image_path
            )
            .returning(UsersOrm)
        )
        await db.commit()

    access_token = create_access_token({"user_id": user_by_google_id.id})
    refresh_token = create_refresh_token({"user_id": user_by_google_id.id})

    response_frontend = RedirectResponse(url=settings.FRONTEND_DOMAIN, status_code=302)

    response_frontend.set_cookie("access_token", access_token)
    response_frontend.set_cookie("refresh_token", refresh_token)

    return response_frontend