from rest_framework import permissions


class IsValidUser(permissions.IsAuthenticated, permissions.BasePermission):
    """ Allow access to valid user, is active"""
    def has_permission(self, request, view):
        return super(IsValidUser, self).has_permission(request, view)\
            and request.user.is_valid


class IsDevUser(IsValidUser):
    """Allow access only to development user"""
    def has_permission(self, request, view):
        return super(IsDevUser, self).has_permission(request, view)\
            and request.user.is_dev


class IsManagerUser(IsValidUser):
    """Allow access only to Manager user"""
    def has_permission(self, request, view):
        return super(IsManagerUser, self).has_permission(request, view)\
            and request.user.is_manager


class IsSuperUser(IsValidUser):
    """Allow access only to Admin user"""
    def has_permission(self, request, view):
        return  super(IsSuperUser, self).has_permission(request, view)\
            and request.user.is_superuser


class UserReadOnly(IsValidUser):
    def has_permission(self, request, view):
        if IsValidUser.has_permission(self, request, view)\
                and request.method in permissions.SAFE_METHODS:
            return True
        else:
            return UserReadOnly.has_permission(self, request, view)


class IsCurrentUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
