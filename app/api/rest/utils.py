import os
from datetime import datetime, timedelta, timezone

import aiofiles
import cv2
import jwt
import numpy as np
from fastapi import HTTPException
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from passlib.context import CryptContext
from PIL import Image
from sklearn.cluster import KMeans

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

serializer = URLSafeTimedSerializer(secret_key=settings.JWT_SECRET_KEY)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire, "sub": "access"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire, "sub": "refresh"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def encode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token has expired")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def save_file(file, path):
    async with aiofiles.open(path, "wb") as new_file:
        while chunk := file.read(1024 * 64):  # Читаем файл частями
            await new_file.write(chunk)


async def save_file_bytes(file_content: bytes, path: str):
    async with aiofiles.open(path, "wb") as new_file:
        await new_file.write(file_content)  # Записываем весь файл сразу



async def delete_file(path):
    try:
        os.remove(path)  # Удаление файла — это синхронная операция, но она обычно очень быстрая
    except FileNotFoundError:
        pass


def create_url_safe_token(data: dict, expiration=3600):
    return serializer.dumps(data)


def decode_url_safe_token(token: str, max_age=3600):
    try:
        token_data = serializer.loads(token, max_age=max_age)
        return token_data
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="Token has expired")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid token")


def get_primary_color(image_path, n_colors=1):
    image = Image.open(image_path)

    if getattr(image, "is_animated", False):
        image.seek(0)

    image = image.convert("RGB")

    image_array = np.array(image)
    pixels = image_array.reshape(-1, 3)

    kmeans = KMeans(n_clusters=n_colors, random_state=42)
    kmeans.fit(pixels)
    dominant_color = kmeans.cluster_centers_[0]

    return tuple(map(int, dominant_color))


def extract_first_frame(video_path, output_image_path=None):
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        raise ValueError(f"Cannot open video file: {video_path}")

    success, frame = video.read()
    if not success:
        raise ValueError(f"Cannot read the first frame from {video_path}")

    if output_image_path:
        cv2.imwrite(output_image_path, frame)

    video.release()

    return frame
