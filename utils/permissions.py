from rest_framework import permissions
from rest_framework.views import Request, View


class IsStaff(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:

        return request.user.is_authenticated and request.user.is_staff
