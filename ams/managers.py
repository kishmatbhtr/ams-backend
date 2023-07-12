from typing import Any

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email: str, password: str, **extra_fields: Any):
        self.create_user

        if not email:
            raise ValueError("Email must be provided")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_user(self, email: str, password: str, **extra_fields: Any):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields: Any):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        self._create_user(email, password, **extra_fields)
