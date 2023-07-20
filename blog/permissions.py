from rest_framework import permissions

"""
This file contains custom permissions used in the blog app.
"""


class IsPostOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.profile.role == 'Admin' or request.user.is_staff


class IsAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role == 'Author' or request.user.is_staff


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role == 'Admin' or request.user.is_staff


class IsReactionOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
