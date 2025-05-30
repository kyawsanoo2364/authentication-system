from rest_framework.generics import GenericAPIView
from .serializers import (
    RegisterSerializer,
    VerifyEmailSerializer,
    LoginSerializer,
    ResetPasswordRequestSerializer,
    SetNewPasswordSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = serializer.data

            return Response(
                {"data": data, "message": "User register successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailAPIView(GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"message": "verified your email successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.error_messages, status=400)


class LoginUserAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            return Response(
                {"data": data, "message": "User Login Successfully!"}, status=200
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "It's ok."}, status=200)


class ResetPasswordRequestAPIView(GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"message": "we sent password reset link.Please check your mail."},
                status=200,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"message": "Reset Password successfully."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutUserAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data["refresh"]
        if not refresh_token:
            return Response({"message": "Refresh token is required"}, status=400)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout Successfully."}, status=200)
        except Exception as e:

            return Response({"message": "Token is invalid"}, status=400)
