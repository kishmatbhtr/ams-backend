import base64
import uuid

from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from backend.configurations.ams_expection import AMSException

from .models import PunchIn, PunchOut, User, UserProfile
from .serializers import (
    LoginSerializer,
    LoginTokenSerializer,
    PunchInSerializer,
    PunchOutSerializer,
    UserProfileSerializer,
    UserSerializer,
)
from .utils import decode_base64_qrimage_data, generate_qr_image, upload_image_to_minio


def home(request):
    return HttpResponse("Hello1")


class UserPagination(PageNumberPagination):
    page_size = 10  # Number of records to display per page
    page_size_query_param = "page_size"
    max_page_size = 100  # Maximum page size allowed


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = UserPagination

    def list(self, reqeust):
        users = User.objects.filter(role=3)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


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
                "role": user.role,
            }
            return Response(response_data)

        else:
            raise AuthenticationFailed()


class PunchInView(viewsets.ModelViewSet):
    queryset = PunchIn.objects.all()
    serializer_class = PunchInSerializer
    permission_classes = [permissions.AllowAny]


class PunchOutView(viewsets.ModelViewSet):
    queryset = PunchOut.objects.all()
    serializer_class = PunchOutSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]


@permission_classes([permissions.IsAuthenticated])
@api_view(["POST"])
def upload_profile_img(request):
    image_bytes = request.data["profile_img"]
    user = request.user
    print(user)
    profile = UserProfile.objects.get_or_create(user=user)
    image = upload_image_to_minio(image_bytes, user.first_name + "profile-img.png")
    profile[0].qr_image = image
    profile.save()

    print(profile[0].user)

    return Response(
        {"message": "Profile Pic Uploaded successfully", "userId": user.id},
        status.HTTP_200_OK,
    )


@permission_classes([permissions.IsAuthenticated])
@api_view(["POST"])
def upload_identity_doc(request):
    # image_bytes = request.data["identity-doc"]
    user = request.user
    print(user)
    # profile = UserProfile.objects.get_or_create(user=user)
    # profile.qr_image = upload_image_to_minio(
    #     image_bytes, user.first_name + "identity-doc.pdf"
    # )
    # profile.save()

    # print(profile[0].user)

    return Response(
        {"message": "Identity Doc Uploaded successfully", "userId": user.id},
        status.HTTP_200_OK,
    )


@permission_classes([permissions.IsAdminUser])
@api_view(["GET"])
def generate_qr_view(request, pk):
    user = User.objects.get(id=pk)
    profile = UserProfile.objects.get_or_create(user=user)
    profile[0].qr_image = generate_qr_image(user.email, user.first_name)
    profile[0].save()

    return Response(
        {"message": "QR Generated Successfully", "userId": user.id}, status.HTTP_200_OK
    )


@api_view(["POST"])
def updateUserData(request):
    """
    {
    "id": 6,
    "password": "apple456",
    "role": 3,
    "profile_img": "base64",
    "identity_doc": "base64"
    }
    """
    user = User.objects.get(id=request.data["id"])

    if len(request.data["password"]) != 0:
        user.set_password(request.data["password"])
    if request.data["role"]:
        user.role = request.data["role"]
    user.save()

    profile = UserProfile.objects.get_or_create(user=user)
    random_4digit: str = str(uuid.uuid4().fields[-1])[:4]
    try:
        if request.data["profile_img"]:
            image_str = request.data["profile_img"]
            image_bytes = base64.b64decode(image_str)
            image = upload_image_to_minio(
                image_bytes, user.first_name + random_4digit + "profile-img.png"
            )
            profile[0].profile_img = image
            profile[0].save()
    except:
        pass

    try:
        if request.data["identity_doc"]:
            doc_str = request.data["identity_doc"]
            doc_bytes = base64.b64decode(doc_str)  # convert to bytes
            profile[0].identity_doc = upload_image_to_minio(
                doc_bytes, user.first_name + random_4digit + "identity_doc.pdf"
            )
            profile[0].save()
    except:
        pass

    return Response(
        {"message": "User Updated Successfully", "userId": user.id}, status.HTTP_200_OK
    )


@permission_classes([permissions.IsAuthenticated])
@api_view(["POST"])
def verify_qr(request):
    """
    {
        "qr_image":"base64-image-data",
    }
    """

    user = request.user
    qr_image = request.data["qr_image"]

    qr_data = decode_base64_qrimage_data(qr_image)

    if user.email == qr_data:
        PunchIn.objects.create(user=user)
        return Response({"message": "Punch In Successfully"}, status.HTTP_201_CREATED)
    else:
        raise AMSException(message="QR Data do not match")
