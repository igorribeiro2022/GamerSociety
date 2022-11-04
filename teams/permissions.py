from rest_framework import permissions
from users.models import User
from teams.models import Team


class IsStaff(permissions.BasePermission):
    # def has_object_permission(self, request, view, obj):
    #     if request.method == 'PATCH' or 'DELETE':
    #         return bool(request.user.is_staff == True)
    #     return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        if request.method == "PATCH" or "DELETE":
            if request.user.is_team_owner == True:
                return bool(request.user.team_id == obj.id)
            return bool(request.user.is_staff)


class TeamPlayers(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "PATCH":
            return bool(obj.users.count() <= 6)


class isAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return bool(request.user.is_authenticated)


class AlreadyHaveATeam(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.user.team_id != None:
            return False

        return True


class PlayerToBeAddedAlreadyHasATeam(permissions.BasePermission):
    def has_permission(self, request, view):
        for key, value in request.data.items():
            user = User.objects.get(username=value)
            if user.team_id != None:
                return False
        return True


class CanReallyAddThisUsersInTeam(permissions.BasePermission):
    def has_object_permission(self, request, view, team: Team):
        players_on_team = team.users.count()
        players_to_add_team = 0
        for key, value in request.data.items():
            players_on_team += 1

        return players_on_team + players_to_add_team <= 6
