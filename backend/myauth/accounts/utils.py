import random
from .models import OneTimePassword, User
from django.core.mail import EmailMessage
from django.conf import settings


def generateOTP():
    code = ""
    for _ in range(6):
        code += str(random.randint(0, 9))
    return code


def send_code_to_user(email):
    user = User.objects.get(email=email)
    otp_code = generateOTP()
    OneTimePassword.objects.create(user=user, code=otp_code)
    emailMessage = EmailMessage(
        subject="Email Verification",
        body=f"Welcome to my authentication project, here verify otp code: {otp_code}",
        from_email=settings.FROM_EMAIL,
        to=[email],
    )
    emailMessage.send(fail_silently=True)


def send_reset_link_to_user(email, link):
    emailMessage = EmailMessage(
        subject="Reset Password",
        body=f"Hello, Welcome back to my authentication project. Here your reset link: {link}",
        from_email=settings.FROM_EMAIL,
        to=[email],
    )
    emailMessage.send(fail_silently=True)
