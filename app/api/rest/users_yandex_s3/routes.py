import hashlib
from io import BytesIO

import aioboto3
from botocore.config import Config
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse

from app.config import settings

router = APIRouter(prefix="/yandex/s3", tags=["yandex-s3"])


@router.post("/upload/")
async def upload_file(file: UploadFile):
    """Загрузка файла в Yandex Object Storage"""
    session = aioboto3.Session()

    try:
        async with session.client(
            "s3",
            endpoint_url="https://storage.yandexcloud.net",
            aws_access_key_id=settings.YANDEX_STORAGE_KEY,
            aws_secret_access_key=settings.YANDEX_STORAGE_SECRET_KEY,
            region_name="ru-central1",
            config=Config(signature_version="s3v4"),  # Включаем подпись S3v4
        ) as s3_client:
            file_content = await file.read()
            file_stream = BytesIO(file_content)  # Используем BytesIO

            # Генерируем SHA256 хеш вручную
            sha256_hash = hashlib.sha256(file_content).hexdigest()

            await s3_client.put_object(
                Bucket=settings.YANDEX_STORAGE_BUCKET,
                Key=file.filename,
                Body=file_stream,
                ContentType=file.content_type,
                ChecksumSHA256=sha256_hash,  # Передаём явный SHA256 хеш
            )
        return JSONResponse(
            content={"message": f"Файл {file.filename} успешно загружен"}, status_code=200
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка загрузки файла: {str(e)}")


@router.get("/download/{filename}")
async def download_file(filename: str):
    """Скачивание файла из Yandex Object Storage"""
    session = aioboto3.Session()

    try:
        async with session.client(
            "s3",
            endpoint_url="https://storage.yandexcloud.net",
            aws_access_key_id=settings.YANDEX_STORAGE_KEY,
            aws_secret_access_key=settings.YANDEX_STORAGE_SECRET_KEY,
            region_name="ru-central1",
            config=Config(signature_version="s3v4"),
        ) as s3_client:
            response = await s3_client.get_object(
                Bucket=settings.YANDEX_STORAGE_BUCKET, Key=filename
            )
            file_data = await response["Body"].read()

            # Определяем MIME-тип по расширению
            file_extension = filename.split(".")[-1].lower()
            media_types = {
                "jpg": "image/jpeg",
                "jpeg": "image/jpeg",
                "png": "image/png",
                "gif": "image/gif",
                "pdf": "application/pdf",
                "mp4": "video/mp4",
                "txt": "text/plain",
            }
            media_type = media_types.get(file_extension, "application/octet-stream")

        return StreamingResponse(
            BytesIO(file_data),
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка скачивания файла: {str(e)}")
