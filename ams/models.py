from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    ADMIN = 1
    MANAGER = 2
    USER = 3

    ROLE_CHOICES = (
        (ADMIN, "ADMIN"),
        (MANAGER, "MANAGER"),
        (USER, "USER"),
    )

    first_name = models.CharField(max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(unique=True)
    password = models.CharField(null=False, blank=False, max_length=200)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=USER)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email


class UserProfile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_img = models.URLField(max_length=200)

    def __str__(self) -> str:
        return self.profile_img


class PunchIn(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    checkin_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user
