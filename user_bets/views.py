from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import UserBet
from .serializers import UserBetCreateSerializer
from rest_framework import generics
from games.models import Game
from teams.models import Team
from django.shortcuts import get_object_or_404
from .permissions import HasMoneyToBet, UserToBetIsInGame, TeamToBetWillPlayInGame

class CreateUserBetView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HasMoneyToBet, UserToBetIsInGame, TeamToBetWillPlayInGame]
    lookup_url_kwarg = "game_id"
    queryset = UserBet.objects.all()
    serializer_class = UserBetCreateSerializer
    
    def perform_create(self, serializer):
        game_id = self.kwargs['game_id']
        team_id = self.kwargs['team_id']
        game = get_object_or_404(Game, id=game_id)
        team = get_object_or_404(Team, id=team_id)
        self.check_object_permissions(self.request, game)
        return serializer.save(game=game, team=team, user=self.request.user)
