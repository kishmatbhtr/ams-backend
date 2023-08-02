from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from . import views as v

router = routers.DefaultRouter()
router.register("user", v.UserView)
router.register("punchin", v.PunchInView)
router.register("punchout", v.PunchOutView)
router.register("userprofile", v.UserProfileView)


urlpatterns = [
    path("a", v.home, name="user"),
    path("", include(router.urls)),
    path("login/", v.LoginView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("gen-qr/<str:pk>", v.generate_qr_view),
    path("profile-img/", v.upload_profile_img),
    path("identity-doc/", v.upload_identity_doc),
    path("update-user/", v.updateUserData),
    path("verify-qr/", v.verify_qr),
    path("reset-password/", v.reset_password),
    path("create-punchout/", v.punchout),
]
