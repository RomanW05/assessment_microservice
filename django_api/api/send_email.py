from django.core.mail import send_mail
from django.conf import settings


def send_otp(otp, user_email):
    message = f'{otp}'
    subject = "validation email"
    send_mail(
        subject,
        message,
        f'{settings.EMAIL_HOST_USER}',
        [f'{user_email}'],
        fail_silently=False,
    )
