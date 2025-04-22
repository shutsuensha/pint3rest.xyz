import mimetypes
from pathlib import Path

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.config import settings

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
    TEMPLATE_FOLDER=Path(__file__).parent / "templates",
)

mail = FastMail(config=mail_config)


def create_message(
    recipients: list[str], subject: str, context: dict, attachment: str | None = None
):
    if attachment:
        message = MessageSchema(
            recipients=recipients,
            subject=subject,
            template_body=context,
            subtype=MessageType.html,
            attachments=[
                {
                    "file": attachment,
                    "headers": {
                        "Content-ID": f"<{attachment.split('/')[-1]}@fastapi-mail>",  # Dynamically generate content ID
                        "Content-Disposition": f"attachment; filename=\"{attachment.split('/')[-1]}\"",
                    },
                    "mime_type": mimetypes.guess_type(attachment)[0]
                    or "application/octet-stream",  # Guess MIME type
                    "mime_subtype": mimetypes.guess_type(attachment)[0].split("/")[1]
                    if mimetypes.guess_type(attachment)[0]
                    else "octet-stream",
                }
            ],
        )
    else:
        message = MessageSchema(
            recipients=recipients, subject=subject, template_body=context, subtype=MessageType.html
        )
    return message
