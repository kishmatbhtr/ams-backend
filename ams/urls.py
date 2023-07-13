from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from . import views as v

router = routers.DefaultRouter()
router.register("user", v.UserView)
router.register("punchin", v.PunchInView)


urlpatterns = [
    path("a", v.home, name="user"),
    path("", include(router.urls)),
    path("login/", v.LoginView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
