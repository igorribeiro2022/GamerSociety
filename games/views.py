from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from utils.permissions import IsStaff
from utils.mixins import SerializerByMethodMixin

from .models import Game
from .serializers import GamesSerializer, GameUpdateSerializer


class ListGamesView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GamesSerializer


class RetrieveUpdateDeleteGameView(
    SerializerByMethodMixin, generics.RetrieveUpdateDestroyAPIView
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff]

    queryset = Game.objects
    serializer_map = {
        "GET": GamesSerializer,
        "PATCH": GameUpdateSerializer,
        "DELETE": GamesSerializer,
    }
