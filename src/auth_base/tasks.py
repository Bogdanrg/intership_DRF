import os

from celery import shared_task
from django.core.mail import send_mail
from dotenv import load_dotenv

load_dotenv()


@shared_task(bind=True)
def send_notification_mail(self: object, target_mail: str, username: str) -> str:
    mail_subject = "Activate your account!"
    send_mail(
        subject=mail_subject,
        message=f"127.0.0.1:8000/api/auth-custom/verification/{username}",
        from_email=os.getenv("EMAIL_HOST_USER"),
        recipient_list=[target_mail],
        fail_silently=False,
    )
    return "Done"


@shared_task(bind=True)
def send_change_password_mail(self: object, target_mail: str, message: str) -> str:
    mail_subject = "Reset your password!"
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=os.getenv("EMAIL_HOST_USER"),
        recipient_list=[target_mail],
        fail_silently=False,
    )
    return "Done"
