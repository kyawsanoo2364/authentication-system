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
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

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
