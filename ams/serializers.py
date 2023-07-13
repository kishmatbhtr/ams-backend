from typing import Dict

import qrcode
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import PunchIn, User
from .utils import image_to_bytes, upload_image_to_minio


def generate_qr_image(user_data, firstName):

    qr_image = qrcode.make(user_data)
    image_bytes = image_to_bytes(qr_image)
    image_url = upload_image_to_minio(image_bytes, firstName)

    return image_url


class LoginSerializer(serializers.Serializer):
    """This is only for documentation"""

    email = serializers.CharField()
    password = serializers.CharField()


class LoginTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "password")
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

        # image_url = generate_qr_image(user.email, user.first_name)

        # profile = UserProfile(user=user, profile_img=image_url)
        # profile.save()

        return user


class PunchInSerializer(serializers.ModelSerializer):
    class Meta:

        model = PunchIn
        fields = "__all__"
