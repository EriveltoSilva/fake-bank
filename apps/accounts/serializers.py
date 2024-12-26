""" serializer file for user data"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from . import emails, validators
from .models import Profile

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer for jwt tokenization"""

    @classmethod
    def get_token(cls, user) -> Token:
        token = super().get_token(user)
        token["user"] = {
            "uid": str(user.uid),
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "vendor_id": user.vendor.vid if hasattr(user, "vendor") else 0,
        }
        try:
            token["user"]["vendor_id"] = user.vendor.vid
        except AttributeError:
            token["user"]["vendor_id"] = 0
        return token


class UserRegisterSerializer(serializers.ModelSerializer):
    """serializer for user registration"""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirmation_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "full_name",
            "email",
            "username",
            "phone",
            "password",
            "confirmation_password",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True

    def validate(self, attrs):
        """validate email and password"""
        errors_messages = {}

        if not validators.is_email_valid(attrs.get("email").strip()):
            errors_messages["email"] = "Este e-mail tem um formato inválido"

        if not validators.is_password_equal(attrs["password"], attrs["confirmation_password"]):
            errors_messages["password"] = errors_messages["confirmation_password"] = "As senhas são diferentes"

        if errors_messages:
            raise serializers.ValidationError(errors_messages)
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirmation_password")
        user = User.objects.create_user(**validated_data)

        email_user, _ = user.email.split("@")
        user.username = validated_data["username"] if validated_data["username"] else email_user
        user.set_password(validated_data["password"])
        user.save()
        link = settings.APPLICATION_FRONTEND_LOGIN_URL
        try:
            if not settings.DEBUG:
                emails.send_register_welcome(user, action_url=link)
        except Exception as e:
            print("Error sending email", e)
        finally:
            print("#" * 100, link, "#" * 100, sep="\n")
        return user


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    # profile = ProfileSerializer(read_only=True)

    class Meta:
        """Meta properties for user serialization"""

        model = User
        fields = (
            "uid",
            "full_name",
            "email",
            "username",
            "phone",
            "password",
            "profile",
        )
        read_only_fields = (
            "uid",
            "profile",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }


class ProfileSerializer(serializers.ModelSerializer):
    """Profile serializer"""

    class Meta:
        """Meta properties for profile serialization"""

        model = Profile
        fields = (
            "pid",
            "full_name",
            "bio",
            "birthday",
            "gender",
            "image",
            # "phone",
            "country",
            "state",
            "city",
            "address",
            "user",
        )
        read_only_fields = ("pid", "user")

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["user"] = UserSerializer(instance.user).data
        return response
