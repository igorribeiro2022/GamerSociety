from rest_framework import permissions
from rest_framework.views import Request, View
from games.models import Game

class IsStaffCampOwner(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, game: Game
    ) -> bool:

        return (
            request.user.is_authenticated
            and game.championship.staff_owner == request.user
        )
        
class HasTeamsOnGame(permissions.BasePermission):
    def has_object_permission(self, request, view, game: Game):
        
        has_team_1 = True
        has_team_2 = True
        if game.team_1 == None:
            has_team_1 = False
        if game.team_2 == None:
            has_team_2 = False
            
        
        return (has_team_1 and has_team_2)