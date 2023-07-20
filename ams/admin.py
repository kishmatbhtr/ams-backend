from django.contrib import admin

from .models import PunchIn, User, UserProfile

# Register your models here.

admin.site.register(User)
admin.site.register(PunchIn)
admin.site.register(UserProfile)
