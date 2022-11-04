from rest_framework import permissions
from rest_framework.views import Request, View
from games.models import Game

class IsStaffCampOwner(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, game: Game
    ) -> bool:

        return (
            request.user.is_authenticated
            and game.championship.staff_owner == request.user.id
        )