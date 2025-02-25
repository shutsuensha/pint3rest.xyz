from fastapi import APIRouter
from app.config import settings
from app.httpx.app import get_httpx_client


router = APIRouter(prefix="/users/google/auth", tags=["users-google-auth"])


@router.get("/login/")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.GOOGLE_OAUTH2_CLIENT_ID}&redirect_uri={settings.GOOGLE_OAUTH2_REDIRECT_URI}&scope=openid%20profile%20email&=offline"
    }


@router.get("/")
async def auth_google(code: str):
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

    user_info = await client.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    
    return user_info.json()