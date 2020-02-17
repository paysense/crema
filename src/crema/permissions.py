from django.conf import settings
from rest_framework import permissions


class InternalTokenRequired(permissions.BasePermission):
    def has_permission(self, request, view):
        token = request.META.get("HTTP_TOKEN")
        return token == settings.INTERNAL_TOKEN
