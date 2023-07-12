from typing import Dict

from rest_framework import serializers

from .models import PunchIn, User


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
        user.save()

        return user


class PunchInSerializer(serializers.ModelSerializer):
    class Meta:

        model = PunchIn
        fields = "__all__"
