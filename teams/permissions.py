from rest_framework import permissions
from django.shortcuts import get_object_or_404

class IsStaff(permissions.BasePermission):
    # def has_object_permission(self, request, view, obj):
    #     if request.method == 'PATCH' or 'DELETE':
    #         return bool(request.user.is_staff == True)
    #     return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.method == 'PATCH' or 'DELETE':
            if request.user.is_team_owner == True:
                return bool(request.user.team_id == obj.id)
            return bool(request.user.is_staff)

class isAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return bool(request.user.is_authenticated)