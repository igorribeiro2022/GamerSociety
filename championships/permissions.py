from rest_framework import permissions
from rest_framework.views import Request, View, status
from championships.models import Championship
from teams.models import Team

from datetime import datetime


class IsChampionshipOwner(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, champs: Championship
    ) -> bool:
        self.message = "You're not the championship owner to perform this action"
        return request.user.is_authenticated and request.user == champs.staff_owner


class IsATeamOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, team: Team) -> bool:
        self.message = "You're not a team owner to perform this action"
        check_owner = False

        for user in team.users.all():
            if user.id == request.user.id and user.is_team_owner:
                check_owner = True

        return check_owner


class HaveFivePlayers(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, team: Team) -> bool:
        self.message = "Your team must have at least 5 players"

        team_players_length = team.users.count()

        return team_players_length >= 5


class IsTeamEsportCorrectly(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, team: Team) -> bool:
        self.message = "Your team do not have same e-sport"

        cs_id = view.kwargs["cs_id"]
        champ = Championship.objects.get(id=cs_id)

        return team.e_sports == champ.e_sport


class IsChampionshipFull(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, team: Team) -> bool:
        self.message = "The championship is full"

        cs_id = view.kwargs["cs_id"]
        champ = Championship.objects.get(id=cs_id)

        number_teams = champ.teams.count()

        return number_teams < 8


class HasAnotherChampionshipAroundSevenDays(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, team: Team) -> bool:
        self.message = "You've other championship around this championship date"

        day_7_in_seconds = 604800

        if team.championship.count() == 0:
            return True

        championship_id = view.kwargs["cs_id"]
        championship = Championship.objects.get(id=championship_id)
        champ_date = datetime(championship.initial_date.year, championship.initial_date.month, championship.initial_date.day)
        championship_date_in_seconds = champ_date.timestamp()

        team_championships_date = team.championship.values("initial_date")
        for initial_date in team_championships_date:
            initial_datetime = datetime(initial_date['initial_date'].year,
                            initial_date['initial_date'].month,
                            initial_date['initial_date'].day
                        )
            initial_datetime_seconds = initial_datetime.timestamp()
            diference_date = abs(championship_date_in_seconds - initial_datetime_seconds)

            if diference_date < day_7_in_seconds:
                return False
            
        return True


class IsChampOwnerTryngToEnterInIt(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, team: Team) -> bool:
        self.message = "Championship owner can't play it"
        cs_id = view.kwargs["cs_id"]
        champ = Championship.objects.get(id=cs_id)
        champ_owner_id = champ.staff_owner.id

        for user in team.users.all():
            if user.id == champ_owner_id:
                return False

        return True
