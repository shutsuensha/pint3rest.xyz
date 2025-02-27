from io import BytesIO

from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.config import settings
from app.yandex_s3.app import get_s3_client

router = APIRouter(prefix="/yandex/s3", tags=["yandex-s3"])


@router.post("/upload/")
async def upload_file(file: UploadFile):
    try:
        s3_client = get_s3_client()
        file_content = await file.read()
        await s3_client.put_object(
            Bucket=settings.YANDEX_STORAGE_BUCKET,
            Key=file.filename,
            Body=file_content,
            ContentType=file.content_type,
        )
        return {"message": f"Файл {file.filename} успешно загружен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{filename}")
async def download_file(filename: str):
    try:
        s3_client = get_s3_client()
        response = await s3_client.get_object(Bucket=settings.YANDEX_STORAGE_BUCKET, Key=filename)
        file_data = await response["Body"].read()

        file_extension = filename.split(".")[-1].lower()
        if file_extension in ["jpg", "jpeg", "png", "gif"]:
            media_type = "image/" + file_extension
        elif file_extension == "pdf":
            media_type = "application/pdf"
        elif file_extension == "mp4":
            media_type = "video/mp4"
        else:
            media_type = "application/octet-stream"

        return StreamingResponse(BytesIO(file_data), media_type=media_type)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
