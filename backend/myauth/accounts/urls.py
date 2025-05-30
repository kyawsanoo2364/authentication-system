from django.urls import path
from .views import (
    RegisterAPIView,
    VerifyEmailAPIView,
    LoginUserAPIView,
    TestView,
    ResetPasswordRequestAPIView,
    SetNewPasswordAPIView,
    LogoutUserAPIView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("verify/", VerifyEmailAPIView.as_view(), name="verify-email"),
    path("login/", LoginUserAPIView.as_view(), name="login"),
    path(
        "reset/password/", ResetPasswordRequestAPIView.as_view(), name="reset-password"
    ),
    path(
        "reset/set-new-password/", SetNewPasswordAPIView.as_view(), name="new-password"
    ),
    path("logout/", LogoutUserAPIView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path("profile/", TestView.as_view(), name="granted"),
]
