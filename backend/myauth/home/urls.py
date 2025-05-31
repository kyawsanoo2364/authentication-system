from django.urls import path
from .views import index

urlpatterns = [
    path("", index, name="index"),
    path("login", index, name="login-frontend"),
    path("register/", index, name="register-frontend"),
    path("reset/", index, name="reset-frontend"),
    path("verify-email/", index, name="verifyeamil-frontend"),
    path("auth/<uidb64>/<token>/", index, name="reset-confirm-password-frontend"),
]
