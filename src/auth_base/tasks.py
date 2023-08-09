from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

import constants


@shared_task(bind=True)
def send_notification_mail(self: object, target_mail: str, username: str) -> str:
    mail_subject = constants.MAIL_SUBJECT_ACTIVATION
    send_mail(
        subject=mail_subject,
        message=f"{constants.MAIL_RESET_VERIFICATION_URL}{username}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[target_mail],
        fail_silently=False,
    )
    return "Done"


@shared_task(bind=True)
def send_change_password_mail(self: object, target_mail: str, message: str) -> str:
    mail_subject = constants.MAIL_SUBJECT_ACTIVATION_PASSWORD_RESET
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[target_mail],
        fail_silently=False,
    )
    return "Done"
