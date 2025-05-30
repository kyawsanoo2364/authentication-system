from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from google.oauth2 import id_token
from django.conf import settings
from google.auth.transport import requests
from accounts.models import User


class GoogleAPISerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        token = attrs["token"]
        if not token:
            raise ValidationError("Google id token is required.")

        try:

            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), audience=settings.GOOGLE_CLIENT_ID
            )
        except:
            raise ValidationError("Invalid token")
        if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            raise ValidationError("Invalid token url.")
        email = idinfo["email"]
        first_name = idinfo["given_name"]
        last_name = idinfo["family_name"]
        try:
            existUser = User.objects.filter(email=email).exists()
            if not existUser:
                newUser = User.objects.create_user(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=settings.SOCIAL_PASSWORD,
                    is_verified=True,
                )
                newUser.save()

                tokens = newUser.token()
                return {
                    "email": newUser.email,
                    "full_name": newUser.get_full_name,
                    "access": tokens["access"],
                    "refresh": tokens["refresh"],
                }
            else:
                user = User.objects.get(email=email)
                tokens = user.token()
                return {
                    "email": user.email,
                    "full_name": user.get_full_name,
                    "access": tokens["access"],
                    "refresh": tokens["refresh"],
                }
        except:
            raise AuthenticationFailed("Sign in failed")
