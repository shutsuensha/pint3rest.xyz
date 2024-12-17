from app.celery.celery_app import celery_instance
from app.mail import mail, create_message
from asgiref.sync import async_to_sync  


@celery_instance.task
def send_email(recipients: list[str], subject: str, body: str):
    message = create_message(recipients=recipients, subject=subject, body=body)
    async_to_sync(mail.send_message)(message)