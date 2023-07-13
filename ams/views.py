from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .models import PunchIn, User, UserProfile
from .serializers import (
    LoginSerializer,
    LoginTokenSerializer,
    PunchInSerializer,
    UserSerializer,
)
from .utils import generate_qr_image


def home(request):
    return HttpResponse("Hello1")


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    # def list(self, reqeust):
    #     users = User.objects.all().order_by("-date_joined")
    #     print(users)
    #     serializer = UserSerializer(users, many=True)
    #     return Response(serializer.data)


class LoginView(CreateAPIView):
    queryset = [
        {"email": "random@test.com"},
        {"password": "password"},
    ]
    serializer_class = LoginSerializer

    def post(self, request):

        email = request.data["email"]
        password = request.data["password"]

        user = authenticate(username=email, password=password)
        if user is not None:

            refresh_token = LoginTokenSerializer.get_token(user)

            response_data = {
                "access": str(refresh_token.access_token),
                "refresh": str(refresh_token),
                "userId": user.id,
                "first_name": user.first_name,
            }
            return Response(response_data)

        else:
            raise AuthenticationFailed()


class PunchInView(viewsets.ModelViewSet):
    queryset = PunchIn.objects.all()
    serializer_class = PunchInSerializer
    permission_classes = [permissions.AllowAny]


@permission_classes([permissions.IsAdminUser])
@api_view(["GET"])
def generate_qr_view(request, pk):

    user = User.objects.get(id=pk)
    profile = UserProfile.objects.get_or_create(user=user)
    # profile.qr_image = generate_qr_image(user.email, user.first_name)
    # profile.save()

    print(profile[0].user)

    return HttpResponse("Success")
