from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets

from apps.accounts.models import CleanerProfile, HostProfile
from apps.accounts.serializers import (
    CleanerProfileSerializer,
    HostProfileSerializer,
    UserSerializer,
)


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_platform_admin:
            return User.objects.all().order_by("id")
        return User.objects.filter(id=user.id)


class HostProfileViewSet(viewsets.ModelViewSet):
    serializer_class = HostProfileSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_platform_admin:
            return HostProfile.objects.select_related("user").all().order_by("id")
        return HostProfile.objects.select_related("user").filter(user=user)


class CleanerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CleanerProfileSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = CleanerProfile.objects.select_related("user").all().order_by("id")
        if user.is_platform_admin or user.is_host:
            return queryset
        return queryset.filter(user=user)

