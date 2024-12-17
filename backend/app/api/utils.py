from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone, date
from app.config import settings
import jwt
from fastapi import HTTPException
import shutil

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def encode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
        raise HTTPException(status_code=401, detail="wrong token or token expire")
    

def save_file(file, path):
    with open(path, "bw+") as new_file:
        shutil.copyfileobj(file, new_file)
