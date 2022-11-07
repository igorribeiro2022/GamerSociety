from .models import User
from .serializers import (
    UserActivitySerializer,
    UserSerializer,
    UserListSerializer,
    UserCreateSerializer,
    SuperUserCreateSerializer,
)
from .permissions import IsAdmin, IsOwnerOrAdmin, IsStaffOrAccountOwner

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import Response, Request
from rest_framework import generics


class ListUsersView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    queryset = User.objects.all()
    serializer_class = UserListSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrAdmin]

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
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)

        return Response({"token": token.key, "user": user_serializer.data})


class CreateSuperUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SuperUserCreateSerializer
