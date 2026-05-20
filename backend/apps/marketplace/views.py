from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from apps.marketplace.models import Assignment, CleanerApplication, CleaningBatch, CleaningJob
from apps.marketplace.serializers import (
    AssignmentSerializer,
    CleanerApplicationSerializer,
    CleaningBatchSerializer,
    CleaningJobSerializer,
)
from apps.marketplace.services import (
    MarketplaceError,
    accept_application,
    complete_job,
    publish_job,
    submit_application,
)


class MarketplaceQuerysetMixin:
    def filter_for_user(self, queryset):
        user = self.request.user
        if user.is_platform_admin:
            return queryset
        if user.is_host:
            return queryset.filter(host=user)
        if user.is_cleaner:
            return queryset.filter(Q(status=CleaningJob.Status.OPEN) | Q(assignment__cleaner=user))
        return queryset.none()


class CleaningBatchViewSet(viewsets.ModelViewSet):
    serializer_class = CleaningBatchSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = CleaningBatch.objects.select_related("property", "host")
        if user.is_platform_admin:
            return queryset
        return queryset.filter(host=user)

    def perform_create(self, serializer):
        property = serializer.validated_data["property"]
        if not (self.request.user.is_platform_admin or self.request.user.is_host):
            raise PermissionDenied("Only hosts can create cleaning batches.")
        if not self.request.user.is_platform_admin and property.host_id != self.request.user.id:
            raise PermissionDenied("Hosts can create batches only for their own properties.")
        serializer.save(host=property.host)


class CleaningJobViewSet(MarketplaceQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = CleaningJobSerializer

    def get_queryset(self):
        queryset = CleaningJob.objects.select_related("property", "host", "batch").prefetch_related(
            "applications"
        )
        return self.filter_for_user(queryset)

    def perform_create(self, serializer):
        property = serializer.validated_data["property"]
        if not (self.request.user.is_platform_admin or self.request.user.is_host):
            raise PermissionDenied("Only hosts can create cleaning jobs.")
        if not self.request.user.is_platform_admin and property.host_id != self.request.user.id:
            raise PermissionDenied("Hosts can create jobs only for their own properties.")
        serializer.save(host=property.host)

    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        try:
            job = publish_job(self.get_object())
        except MarketplaceError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(job).data)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        try:
            job = complete_job(job=self.get_object(), completed_by=request.user)
        except MarketplaceError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(job).data)


class CleanerApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = CleanerApplicationSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = CleanerApplication.objects.select_related("job", "cleaner", "job__host")
        if user.is_platform_admin:
            return queryset
        if user.is_host:
            return queryset.filter(job__host=user)
        if user.is_cleaner:
            return queryset.filter(cleaner=user)
        return queryset.none()

    def perform_create(self, serializer):
        application = submit_application(
            job=serializer.validated_data["job"],
            cleaner=self.request.user,
            proposed_price=serializer.validated_data.get("proposed_price"),
            message=serializer.validated_data.get("message", ""),
        )
        serializer.instance = application

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        try:
            assignment = accept_application(
                application=self.get_object(),
                accepted_by=request.user,
                agreed_price=request.data.get("agreed_price"),
            )
        except MarketplaceError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(AssignmentSerializer(assignment).data, status=status.HTTP_201_CREATED)


class AssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Assignment.objects.select_related("job", "cleaner", "application", "job__host")
        if user.is_platform_admin:
            return queryset
        if user.is_host:
            return queryset.filter(job__host=user)
        if user.is_cleaner:
            return queryset.filter(cleaner=user)
        return queryset.none()
