from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from .permissions import IsStaffCampOwner, HasTeamsOnGame
from .models import Game
from bet_types.models import BetType
from .serializers import (
    GameUpdateSerializer,
    GameWinnerSerializer,
    GamesToBetSerializer,
)
from teams.models import Team
from championships.models import Championship
from utils.game_name_phase import Phase
from users.models import User
from bets.models import Bet
from transactions.serializers import TransactionSerializer


class ListBettableGamesView(generics.ListAPIView):
    queryset = Game.objects.exclude(team_1=None, team_2=None).filter(winner=None)
    serializer_class = GamesToBetSerializer


class UpdateTeamsGameView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaffCampOwner]
    serializer_class = GameUpdateSerializer
    lookup_url_kwarg = "game_id"
    queryset = Game.objects.all()
    
    def patch(self, request, *args, **kwargs):
        game = self.partial_update(request, *args, **kwargs)
        game_obj = Game.objects.get(id=game.data['id'])

        game.data["championship"]
        bet = {
            "team_1": game.data["team_1"],
            "team_2": game.data["team_2"]
        }
        bet_created = Bet.objects.create(**bet, game=game_obj)
        bet_type_1 = {
            "team": game.data["team_1"]
        }
        bet_type_2 = {
            "team": game.data["team_2"]
        }
        BetType.objects.create(**bet_type_1, bet=bet_created)
        BetType.objects.create(**bet_type_2, bet=bet_created)
        
        return game
    


class UpdateGameWinnerView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaffCampOwner, HasTeamsOnGame]
    lookup_url_kwarg = "game_id"
    queryset = Game.objects.all()
    serializer_class = GameWinnerSerializer

    def patch(self, request, *args, **kwargs):
        game = self.partial_update(request, *args, **kwargs)
        # ipdb.set_trace()
        champ = Championship.objects.get(id=game.data["championship"])
        if game.data["winner"] == game.data["team_1"]:
            team_1_winner = Team.objects.get(id=game.data["team_1"])
            team_1_winner.wins += 1
            team_1_winner.save()

            team_2_lost = Team.objects.get(id=game.data["team_2"])
            team_2_lost.losses += 1
            team_2_lost.save()

        team_2_winner = Team.objects.get(id=game.data["team_2"])
        team_2_winner.wins += 1
        team_2_winner.save()

        team_1_lost = Team.objects.get(id=game.data["team_1"])
        team_1_lost.losses += 1
        team_1_lost.save()

        # TEST WITHOUT TEAMS IN GAME
        # team_1_winner = Team.objects.get(id=game.data['winner'])
        # team_1_winner.wins += 1
        # team_1_winner.save()

        # IF IS PHASE FINAL CHAMPIONS GIVE MONEY TO WINNER TEAM OWNER
        if game.data["phase"] == Phase.FINAL_CHAMPIONS:
            winner_team = Team.objects.get(id=game.data["winner"])
            champ.winner = winner_team.id
            champ.save()
            user_to_reward = None

            for user in winner_team.users.all():
                if user.is_team_owner:
                    user_to_reward = User.objects.get(id=user.id)

            prize = {"value": champ.prize}

            trans = TransactionSerializer(data=prize)
            trans.is_valid(raise_exception=True)
            trans.save(user=user_to_reward)

        # ipdb.set_trace()
        # TRIGGER TO CLOSE GAME BET AND GIVE MONEY

        return game
