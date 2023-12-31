from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


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

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    qr_image = models.URLField(max_length=200, default="")
    profile_img = models.URLField(max_length=200, default="")
    identity_doc = models.URLField(max_length=200, default="")

    def __str__(self) -> str:
        return self.user.email


class PunchIn(models.Model):

    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    checkin_time = models.DateTimeField(default="")

    def __str__(self) -> str:
        return self.user.email

    @property
    def punchin_time(self):
        return self.checkin_time.strftime("%A, %b %d %Y, %I:%M %p")



class PunchOut(models.Model):

    user = models.ForeignKey(User, related_name="punchout_user", on_delete=models.CASCADE)
    checkout_time = models.DateTimeField(default="")

    def __str__(self) -> str:
        return self.user.email

    @property
    def punchout_time(self):
        return self.checkout_time.strftime("%A, %b %d %Y, %I:%M %p")