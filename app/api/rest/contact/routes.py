import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.api.rest.utils import save_file
from app.celery.tasks import send_email
from app.config import settings

router = APIRouter(prefix="/contact", tags=["contact"])


@router.post("/")
async def send_contact_form(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    file: Optional[UploadFile] = File(None),
):
    image_path = None
    if file:
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        image_path = f"{settings.MEDIA_PATH}contact/{unique_filename}"

        await save_file(file.file, image_path)

    form_data = {
        "name": name,
        "email": email,
        "message": message,
        "attachment": image_path if image_path else None,
    }

    context = {"name": name, "email": email, "message": message}

    emails = ["dankupr21@gmail.com"]
    subject = "Ryply email from Resume site"
    send_email.delay(emails, subject, context, "reply_from_resume.html", attachment=image_path)

    return JSONResponse(
        content=jsonable_encoder({"status": "success", "data": form_data}), status_code=200
    )
