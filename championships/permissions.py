from rest_framework import permissions
from rest_framework.views import Request, View
from championships.models import Championship


class IsChampionshipOwner(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, champs: Championship
    ) -> bool:

        return (
            request.user.is_authenticated
            and request.user == champs.staff_owner
        )
