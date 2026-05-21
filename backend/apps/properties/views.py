from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from apps.properties.models import ExternalCalendarConnection, Property, Reservation
from apps.properties.serializers import (
    ExternalCalendarConnectionSerializer,
    PropertySerializer,
    ReservationSerializer,
)


class HostOwnedQuerysetMixin:
    def filter_for_user(self, queryset):
        user = self.request.user
        if user.is_platform_admin:
            return queryset
        if not user.is_approved:
            return queryset.none()
        return queryset.filter(property__host=user)


class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Property.objects.select_related("host").all()
        if user.is_platform_admin:
            return queryset
        if not user.is_approved:
            return queryset.none()
        return queryset.filter(host=user)

    def perform_create(self, serializer):
        if not (self.request.user.is_platform_admin or self.request.user.is_host):
            raise PermissionDenied("Only hosts can create properties.")
        if not self.request.user.is_platform_admin and not self.request.user.is_approved:
            raise PermissionDenied("Account must be approved before creating properties.")
        serializer.save(host=self.request.user)


class ExternalCalendarConnectionViewSet(HostOwnedQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = ExternalCalendarConnectionSerializer

    def get_queryset(self):
        queryset = ExternalCalendarConnection.objects.select_related("property", "property__host")
        return self.filter_for_user(queryset)

    def perform_create(self, serializer):
        property = serializer.validated_data["property"]
        if not self.request.user.is_platform_admin and not self.request.user.is_approved:
            raise PermissionDenied("Account must be approved before creating calendar connections.")
        if not self.request.user.is_platform_admin and property.host_id != self.request.user.id:
            raise PermissionDenied("Calendar connections can be created only for owned properties.")
        serializer.save()


class ReservationViewSet(HostOwnedQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        queryset = Reservation.objects.select_related("property", "property__host")
        return self.filter_for_user(queryset)

    def perform_create(self, serializer):
        property = serializer.validated_data["property"]
        if not self.request.user.is_platform_admin and not self.request.user.is_approved:
            raise PermissionDenied("Account must be approved before creating reservations.")
        if not self.request.user.is_platform_admin and property.host_id != self.request.user.id:
            raise PermissionDenied("Reservations can be created only for owned properties.")
        serializer.save()
