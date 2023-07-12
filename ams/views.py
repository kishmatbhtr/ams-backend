from django.http import HttpResponse
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from .models import PunchIn, User
from .serializers import PunchInSerializer, UserSerializer


def home(request):
    return HttpResponse("Hello")


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    # def list(self, reqeust):
    #     users = User.objects.all().order_by("-date_joined")
    #     print(users)
    #     serializer = UserSerializer(users, many=True)
    #     return Response(serializer.data)


class PunchInView(viewsets.ModelViewSet):
    queryset = PunchIn.objects.all()
    serializer_class = PunchInSerializer
    permission_classes = [permissions.AllowAny]
