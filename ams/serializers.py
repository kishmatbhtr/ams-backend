from typing import Dict

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import PunchIn, User, UserProfile


class LoginSerializer(serializers.Serializer):
    """This is only for documentation"""

    email = serializers.CharField()
    password = serializers.CharField()


class LoginTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("id", "profile_img", "qr_image")


class UserSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "role",
            "profile",
        )
        extra_kwargs = {
            "first_name": {"required": "True"},
            "password": {"write_only": "True"},
        }

    def create(self, validated_data: Dict) -> User:

        user = User.objects.create(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user

    # def update(self, instance, validated_data: Dict):

    #     instance.first_name = validated_data.get("first_name", instance.first_name)
    #     instance.last_name = validated_data.get("last_name", instance.last_name)

    #     instance.set_password(validated_data["password"])
    #     instance.save()

    #     return instance


class PunchInSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(
        source="user.email",
    )
    punchin_time = serializers.ReadOnlyField()

    class Meta:

        model = PunchIn
        fields = ("id", "email", "punchin_time", "user")
        extra_kwargs = {
            "user": {"write_only": "True"},
        }


# TODO : create UserProfileSerializer
