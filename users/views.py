from .models import User
from .serializers import (
    UserActivitySerializer,
    UserSerializer,
    UserListSerializer,
    UserCreateSerializer,
    SuperUserCreateSerializer,
)
from .permissions import IsAdmin, IsOwnerOrAdmin, IsStaffOrAccountOwner
from user_bets.models import UserBet
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import Response, Request
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from user_bets.serializers import ListUserBetSerializer


class ListUsersView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    queryset = User.objects.all()
    serializer_class = UserListSerializer
    
class ListUserBetsView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = UserBet.objects.all()
    serializer_class = ListUserBetSerializer
    
    def list(self, request, *args, **kwargs):
        
        user_bets = UserBet.objects.filter(user=request.user.id)
        
        serializer = self.get_serializer(user_bets, many=True)
        return Response(serializer.data)
        


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
