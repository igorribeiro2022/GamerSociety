from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from utils.permissions import IsStaff
from .permissions import IsStaffCampOwner
from utils.mixins import SerializerByMethodMixin
from .models import Game
from .serializers import GameUpdateSerializer, GameWinnerSerializer, GamesToBetSerializer
from teams.models import Team
from championships.models import Championship
from utils.game_name_phase import Phase
from users.models import User
import datetime


class ListBettableGamesView(generics.ListAPIView):
    queryset = Game.objects.exclude(team_1_id=None, team_2_id=None).filter(winner_id=None)
    serializer_class = GamesToBetSerializer
    



class RetrieveUpdateDeleteGameView(SerializerByMethodMixin, generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaffCampOwner]
    lookup_url_kwarg = "game_id"
    queryset = Game.objects.all()
    serializer_map = {
        "PATCH": GameUpdateSerializer,
    }
    
class UpdateGameWinnerView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaffCampOwner]
    lookup_url_kwarg = "game_id"
    queryset = Game.objects.all()
    serializer_class = GameWinnerSerializer
    
    def patch(self, request, *args, **kwargs):
        game = self.partial_update(request, *args, **kwargs)
        champ = Championship.objects.get(id=game.championship.id)
        
        if game.winner == game.team_1:
            team_1_winner = Team.objects.get(id=game.team_1)
            team_1_winner.wins += 1
            team_1_winner.save()
            
            team_2_lost = Team.objects.get(id=game.team_2)
            team_2_lost.losses += 1
            team_2_lost.save()
            
        team_2_winner = Team.objects.get(id=game.team_2)
        team_2_winner.wins += 1
        team_2_winner.save()
        
        team_1_lost = Team.objects.get(id=game.team_1)
        team_1_lost.losses += 1
        team_1_lost.save()
        
        #IF IS PHASE FINAL CHAMPIONS GIVE MONEY TO WINNER TEAM OWNER
        if game.phase == Phase.FINAL_CHAMPIONS:
            winner_team = Team.objects.get(id=game.winner)
            champ.winner = winner_team.id
            user_to_reward = None 
            # user_history = History.objects.get(user=user_to_reward)
            for user in winner_team.users.all():
                if user.is_team_owner:
                    user_to_reward = User.objects.get(id=user.id)
            # transaction = Transaction.objects.create({
            #     "value": champ.prize,
            #     "date": datetime.datetime.now()
            # }, history=user_history)        
            
            
        
        #TRIGGER TO CLOSE GAME BET AND GIVE MONEY
        
        return game
   
