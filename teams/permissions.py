from rest_framework import permissions

class IsStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method is 'PATCH' or 'DELETE':
            return request.user.is_staff == True