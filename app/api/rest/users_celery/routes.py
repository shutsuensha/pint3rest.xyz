import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, status
from sqlalchemy import select

from app.api.rest.dependencies import db
from app.celery.celery_app import celery_instance
from app.celery.tasks import save_file_celery_and_crop_300x300
from app.config import settings
from app.postgresql.models import UsersOrm
from celery.result import AsyncResult

router = APIRouter(prefix="/celery/users", tags=["users-celery"])


@router.post("/upload/{id}")
async def upload_image_celery(id: int, db: db, file: UploadFile):

    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )

    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    image_path = f"{settings.MEDIA_PATH}users/{unique_filename}"

    task = save_file_celery_and_crop_300x300.delay(file.file.read(), image_path, id)

    return {"message": "File upload is in progress", "task_id": task.id}


@router.get("/upload/status/{task_id}")
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
