from app.celery.celery_app import celery_instance
from app.mail.mail import mail, create_message
from asgiref.sync import async_to_sync  


@celery_instance.task
def send_email(recipients: list[str], subject: str, context: dict, template_name: str):
    message = create_message(recipients=recipients, subject=subject, context=context)
    async_to_sync(mail.send_message)(message, template_name=template_name)