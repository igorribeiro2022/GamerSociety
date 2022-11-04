from rest_framework import permissions
from rest_framework.views import Request, View, status
from historys.models import History

class UserIsHistoryOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, his: History) -> bool:
        return (request.user == his.user)