from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import BetSerializer
from games.models import Game
from rest_framework.exceptions import NotFound
import uuid
from bets.models import Bet
from django.shortcuts import get_object_or_404

# class RetrieveBetGameView(generics.RetrieveAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     lookup_url_kwarg = "game_id"
#     serializer_class = BetSerializer

# def get_queryset(self):
#     game_id = self.kwargs['game_id']
#     try:
#         uuid.UUID(game_id, version=4)
#     except ValueError:

#         raise NotFound({"detail": "ID not UUID type"})

#     game = get_object_or_404(Game, id=self.kwargs['game_id'])
#     return Bet.objects.filter(game=game)

# def get_object(self):
#     queryset = self.filter_queryset(self.get_queryset())
#     bet = queryset[0]
#     return bet


class RetrieveBetGameView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "game_id"
    serializer_class = BetSerializer
    queryset = Game.objects.all()

    def get_object(self):
        game_id = self.kwargs["game_id"]
        try:
            uuid.UUID(game_id, version=4)
        except ValueError:

            raise NotFound({"detail": "ID not UUID type"})
        game = get_object_or_404(Game, id=self.kwargs["game_id"])

        bet = get_object_or_404(Bet, game=game)
        return bet
