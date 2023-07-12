from django.urls import include, path
from rest_framework import routers

from . import views as v

router = routers.DefaultRouter()
router.register("user", v.UserView)
router.register("punchin", v.PunchInView)


urlpatterns = [
    path("a", v.home, name="user"),
    path("", include(router.urls)),
]
