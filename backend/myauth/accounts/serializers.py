from rest_framework import serializers
from .models import User, OneTimePassword
from django.core.exceptions import ValidationError
from .utils import send_code_to_user, send_reset_link_to_user
from rest_framework.authentication import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=255, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=255, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "password2"]

    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise ValidationError("User has already exists. Please Log in or verify.")
        if attrs["password"] != attrs["password2"]:
            raise ValidationError("Passwords do not match.")
        if attrs["first_name"] == None or attrs["last_name"] == None:
            raise ValidationError("All fields are required!")

        return attrs

    def create(self, validated_data):
        email = validated_data["email"]
        first_name = validated_data["first_name"]
        last_name = validated_data.get("last_name")
        password = validated_data["password"]

        user = User.objects.create_user(
            email=email, first_name=first_name, last_name=last_name, password=password
        )
        user.save()
        send_code_to_user(user.email)
        return user


class VerifyEmailSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate(self, attrs):
        try:
            otp = OneTimePassword.objects.get(code=attrs["code"])
            if otp:
                user = otp.user
                user.is_verified = True
                user.save()
                return user
            else:
                raise ValidationError("Invalid Code")
        except:
            raise ValidationError("Invalid Code")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        if email is None:
            raise ValidationError("Email is required!")
        if password is None:
            raise ValidationError("Password is required!")

        try:
            existUser = User.objects.filter(email=email).exists()
            if not existUser:
                raise ValidationError("User not found Please create new account.")

            user = authenticate(email=email, password=password)
            if user:
                tokens = user.token()
                email = user.email
                full_name = user.get_full_name
                return {
                    "email": email,
                    "full_name": full_name,
                    "access": tokens["access"],
                    "refresh": tokens["refresh"],
                }
            else:
                raise AuthenticationFailed("Invalid credentials")

        except AuthenticationFailed:
            raise AuthenticationFailed("Invalid credentials")


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs["email"]
        try:
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            resetToken = PasswordResetTokenGenerator().make_token(user)
            relative_path = f"{settings.FRONTEND_URL}/{uidb64}/{resetToken}/"
            send_reset_link_to_user(user.email, link=relative_path)
            return {"email": user.email, "reset_link": relative_path}
        except:
            raise ValidationError("User not found")


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6)
    password2 = serializers.CharField(min_length=6)
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        password = attrs["password"]
        password2 = attrs["password2"]
        uidb64 = attrs["uidb64"]
        token = attrs["token"]

        if password != password2:
            raise ValidationError("Passwords do not match.")

        try:
            user_id = urlsafe_base64_decode(smart_str(uidb64))
            user = User.objects.get(id=user_id)
        except Exception as e:
            raise ValidationError("Invalid User")

        if not PasswordResetTokenGenerator().check_token(user=user, token=token):
            raise ValidationError("Reset token is invalid or has expired.")

        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        password = self.validated_data["password"]
        user.set_password(password)
        user.save()
        return user
