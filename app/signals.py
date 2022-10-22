from django.conf import settings
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives

from app.tasks import send_email

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
    Отправляем письмо с токеном для сброса пароля
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param kwargs:
    :return:
    """
    # send an e-mail to the user

    # msg = EmailMultiAlternatives(
    #     # title:
    #     f"Password Reset Token for {reset_password_token.user}",
    #     # message:
    #     reset_password_token.key,
    #     # from:
    #     settings.EMAIL_HOST_USER,
    #     # to:
    #     [reset_password_token.user.email]
    # )
    # msg.send()

    title = f"Password Reset Token for {reset_password_token.user}"
    message = reset_password_token.key
    email = reset_password_token.user.email
    send_email.delay(title=title, message=message, email=email)

