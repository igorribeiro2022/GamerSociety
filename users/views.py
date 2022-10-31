from rest_framework import generics
from users.models import User
from users.serializers import UserActivitySerializer, UserSerializer, UserListSerializer
from .permissions import IsStaffOrCreateOnly, IsAccountOwner, IsStaffOrAccountOwner
from rest_framework.authentication import TokenAuthentication
from utils.mixins import SerializerByMethodMixin

class ListCreateUserView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaffOrCreateOnly]
    queryset = User.objects.all()
    
    serializer_map = {
        "GET": UserListSerializer,
        "POST": UserSerializer,
    }
    
class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAccountOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UpdateActivityUserView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaffOrAccountOwner]
    queryset = User.objects.all()
    serializer_class = UserActivitySerializer

