from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User


class IsStaff(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:

        return request.user.is_authenticated and request.user.is_staff


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, user: User
    ) -> bool:

        return request.user.is_authenticated and request.user == user


class IsStaffOrAccountOwner(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, user: User
    ) -> bool:

        return (
            request.user.is_authenticated
            and request.user == user
            or request.user.is_staff
        )
