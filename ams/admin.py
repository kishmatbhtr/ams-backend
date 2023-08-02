from django.contrib import admin

from .models import PunchIn, User, UserProfile, PunchOut

# Register your models here.

admin.site.register(User)
admin.site.register(PunchIn)
admin.site.register(PunchOut)
admin.site.register(UserProfile)
