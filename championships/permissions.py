from rest_framework import permissions
from rest_framework.views import Request, View
from championships.models import Championship
from teams.models import Team
import ipdb


class IsChampionshipOwner(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, champs: Championship
    ) -> bool:

        return (
            request.user.is_authenticated
            and request.user == champs.staff_owner
        )

class IsAteamOwnerAndHaveFivePlayers(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, team: Team) -> bool:
            
        check_owner = False
        
        for user in team.users.all():
            if user.id == request.user.id and user.is_team_owner:
                check_owner = True
                
        team_players_length = team.users.count()

        cs_id = view.kwargs['cs_id']
        champ = Championship.objects.get(id=cs_id)
        
        number_teams = champ.teams.count()
        
        return (check_owner and team.e_sports == champ.e_sport and team_players_length>= 5 and number_teams < 8)
    
class HasAnotherChampAroundSevenDays(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, team: Team) -> bool:
        if team.championship.count() == 0:
            return True
        
        
        
        
