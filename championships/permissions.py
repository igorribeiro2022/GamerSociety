from rest_framework import permissions
from rest_framework.views import Request, View
from championships.models import Championship
from teams.models import Team


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
        
        def permission():
            for user in team.users:
                if user.id == request.user.id and user.is_team_owner:
                    return True
            return False
        
        team_players_length = team.users.count()
        
        return (permission and team_players_length >= 5)
    
class HasAnotherChampAroundSevenDays(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, team: Team) -> bool:
        ...
