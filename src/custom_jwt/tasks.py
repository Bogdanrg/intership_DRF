from celery import shared_task
from django.core.mail import send_mail


@shared_task(bind=True)
def send_notification_mail(self, target_mail, username):
    mail_subject = "Activate your account!"
    send_mail(
        subject=mail_subject,
        message=f"127.0.0.1:8000/api/auth-custom/{username}",
        from_email='tsimafeyeu.b@gmail.com',
        recipient_list=[target_mail],
        fail_silently=False,
    )
    return "Done"


@shared_task(bind=True)
def send_change_password_mail(self, target_mail, message):
    mail_subject = "Reset your password!"
    send_mail(
        subject=mail_subject,
        message=message,
        from_email='tsimafeyeu.b@gmail.com',
        recipient_list=[target_mail],
        fail_silently=False,
    )
    return "Done"
