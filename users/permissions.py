from rest_framework import permissions

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        # Only allow access for users with 'student' role
        return request.user.role == 'Student'


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        # Only allow access for users with 'staff' or 'admin' role
        return request.user.role in ['Staff', 'Admin']


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Only allow access for users with 'admin' role
        return request.user.role == 'Admin'
