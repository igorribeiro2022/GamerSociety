from rest_framework import permissions
from rest_framework.views import Request, View
from games.models import Game
from datetime import datetime


class NewClassPermission:
    def has_date_permission(self, request: Request, view: View, game: Game):
        return True


class IsStaffCampOwner(permissions.BasePermission, NewClassPermission):
    def has_object_permission(self, request: Request, view: View, game: Game) -> bool:
        self.message = "You're not the championship owner to perform this action"
        return (
            request.user.is_authenticated
            and game.championship.staff_owner == request.user
        )


class HasTeamsOnGame(permissions.BasePermission, NewClassPermission):
    def has_object_permission(self, request, view, game: Game):
        self.message = "You must edit game teams to set winner one"
        has_team_1 = True
        has_team_2 = True
        if game.team_1 == None:
            has_team_1 = False
        if game.team_2 == None:
            has_team_2 = False

        return has_team_1 and has_team_2


class RequestMethodIsPut(permissions.BasePermission, NewClassPermission):
    def has_permission(self, request: Request, view: View) -> bool:
        self.message = "Only PUT method allowed"
        if request.method == "PATCH":
            return False

        return True


class IsDateAfterChampInitialDate(permissions.BasePermission, NewClassPermission):
    def has_date_permission(self, request: Request, view: View, game: Game):
        self.message = "Game date must be after championship initial date"

        game_data_in_seconds = datetime.strptime(
            request.data["initial_date"], "%Y-%m-%d"
        ).timestamp()

        champ_date = game.championship.initial_date

        champ_date_in_seconds = datetime(
            champ_date.year, champ_date.month, champ_date.day
        ).timestamp()

        return game_data_in_seconds > champ_date_in_seconds
