from championships.models import Championship
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
        self.message = "You must set teams in game firts, to set winner one"
        has_team_1 = True
        has_team_2 = True
        if game.team_1 == None:
            has_team_1 = False
        if game.team_2 == None:
            has_team_2 = False

        return has_team_1 and has_team_2


class IsTeam1And2TheSame(permissions.BasePermission, NewClassPermission):
    def has_permission(self, request, view):
        self.message = "Team_1 and team_2 must be different, check given teams"
        team_1_id = request.data["team_1"]
        team_2_id = request.data["team_2"]
        return team_1_id != team_2_id


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


class IsValidTeam(permissions.BasePermission, NewClassPermission):
    def has_date_permission(self, request: Request, view: View, game: Game) -> bool:
        self.message = "Teams provided are not in championship"
        champ = Championship.objects.get(id=game.championship.id)
        champ_teams = champ.teams.all()
        has_team_1 = False
        has_team_2 = False
        team_1_id = request.data["team_1"]
        team_2_id = request.data["team_2"]
        for team in champ_teams:
            if str(team.id) == team_1_id:
                has_team_1 = True
            elif str(team.id) == team_2_id:
                has_team_2 = True

        return has_team_1 and has_team_2


class IsInitialDateInFuture(permissions.BasePermission, NewClassPermission):
    def has_date_permission(self, request: Request, view: View, game: Game):
        self.message = "Initial date must be future days"
        initial_date_list = request.data["initial_date"].split("-")
        date_now = datetime.now().timestamp()
        game_date = datetime(
            int(initial_date_list[0]),
            int(initial_date_list[1]),
            int(initial_date_list[2]),
        )
        game_date_in_seconds = game_date.timestamp()
        return game_date_in_seconds > date_now


class IsThere8TeamsInCamp(permissions.BasePermission, NewClassPermission):
    def has_object_permission(self, request, view, game: Game):
        self.message = "Championship must be full to init one game, check championship teams, must have eigth"
        champ = Championship.objects.get(id=game.championship.id)
        teams_in_champ = champ.teams.count()
        expected = 8
        return teams_in_champ == expected

class IsWinnerOneOfGameTeams(permissions.BasePermission, NewClassPermission):
    def has_object_permission(self, request: Request, view: View, game: Game):
        self.message = "Winner settled isn't in game"
        winner = request.data['winner']
        return (winner == game.team_1 or winner == game.team_2)