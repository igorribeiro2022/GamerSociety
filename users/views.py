from utils.mixins import SerializerByMethodMixin
from users.models import User
from users.serializers import (
    UserActivitySerializer,
    UserSerializer,
    UserListSerializer,
    UserCreateSerializer,
)
from .permissions import IsStaff, IsAccountOwner, IsStaffOrAccountOwner
from rest_framework.authentication import TokenAuthentication
from utils.mixins import SerializerByMethodMixin
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics
import json


class ListUsersView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff]
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAccountOwner]
    lookup_url_kwarg = "user_id"
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UpdateActivityUserView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaffOrAccountOwner]
    lookup_url_kwarg = "user_id"
    queryset = User.objects.all()
    serializer_class = UserActivitySerializer


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response({"token": token.key, "user": user_serializer.data})
