from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.calendars.services import find_property_job_conflicts
from apps.marketplace.serializers import CleaningJobSerializer


class CalendarConflictView(APIView):
    def get(self, request):
        property_id = request.query_params.get("property_id")
        starts_at = parse_datetime(request.query_params.get("starts_at", ""))
        ends_at = parse_datetime(request.query_params.get("ends_at", ""))

        if not property_id or not starts_at or not ends_at:
            return Response(
                {"detail": "property_id, starts_at, and ends_at query parameters are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conflicts = find_property_job_conflicts(
            property_id=property_id,
            starts_at=starts_at,
            ends_at=ends_at,
        )
        return Response(CleaningJobSerializer(conflicts, many=True).data)

