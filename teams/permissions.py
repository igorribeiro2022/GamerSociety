from rest_framework import permissions
from users.models import User
from teams.models import Team
from django.shortcuts import get_object_or_404


class IsStaff(permissions.BasePermission):
    # def has_object_permission(self, request, view, obj):
    #     if request.method == 'PATCH' or 'DELETE':
    #         return bool(request.user.is_staff == True)
    #     return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        self.message = "You're not team's owner"
        if request.method == "GET":
            return True
        if request.method == "PATCH" or "DELETE":
            if request.user.is_team_owner == True:
                return bool(request.user.team_id == obj.id)
            return bool(request.user.is_staff)


class isAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        self.message = "You're not authenticated"
        if request.method == "GET":
            return True
        return bool(request.user.is_authenticated)


class AlreadyHaveATeam(permissions.BasePermission):
    def has_permission(self, request, view):
        self.message = "You already have a team"
        if request.user.team_id != None:
            return False
        return True


class PlayerToBeAddedAlreadyHasATeam(permissions.BasePermission):
    def has_permission(self, request, view):
        self.message = "Some player that you're tryng to add already has a team"
        for key, value in request.data.items():
            user = get_object_or_404(User, username=value)
            if user.team_id != None:
                return False
        return True


class CanReallyAddThisUsersInTeam(permissions.BasePermission):
    def has_object_permission(self, request, view, team: Team):
        self.message = "You can't add more than 6 players on team"
        players_on_team = team.users.count()
        players_to_add_team = 0
        for key, value in request.data.items():
            players_on_team += 1

        return players_on_team + players_to_add_team <= 6
