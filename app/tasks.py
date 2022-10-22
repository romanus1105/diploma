from diploma.settings import EMAIL_HOST_USER
from django.core.mail.message import EmailMultiAlternatives
from celery import shared_task

@shared_task
def send_email(title, message: str, email: str):
    try:
        message = EmailMultiAlternatives(
            subject=title,
            body=message,
            from_email=EMAIL_HOST_USER,
            to=[email,]
        )
        message.send()
        return f'Title: {message.subject}, Message:{message.body}'
    except Exception:
        raise Exception
