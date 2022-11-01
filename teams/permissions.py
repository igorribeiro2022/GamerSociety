from rest_framework import permissions

class IsStaff(permissions.BasePermission):
    # def has_object_permission(self, request, view, obj):
    #     if request.method == 'PATCH' or 'DELETE':
    #         return bool(request.user.is_staff == True)
    #     return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.method == 'PATCH' or 'DELETE':
            if request.user == obj.owner:
                return True
            return bool(request.user.is_staff)

class isAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return bool(request.user.is_authenticated)