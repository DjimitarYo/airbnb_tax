from rest_framework import serializers

from apps.marketplace.models import Assignment, CleanerApplication, CleaningBatch, CleaningJob
from apps.properties.models import Property


class CleaningBatchSerializer(serializers.ModelSerializer):
    property_id = serializers.PrimaryKeyRelatedField(
        source="property",
        queryset=Property.objects.all(),
        write_only=True,
    )
    host = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CleaningBatch
        fields = [
            "id",
            "property_id",
            "property",
            "host",
            "title",
            "month",
            "status",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "property", "host", "status", "created_at", "updated_at"]


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = [
            "id",
            "job",
            "cleaner",
            "application",
            "agreed_price",
            "assigned_at",
            "cancelled_at",
            "completed_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class CleaningJobSerializer(serializers.ModelSerializer):
    property_id = serializers.PrimaryKeyRelatedField(
        source="property",
        queryset=Property.objects.all(),
        write_only=True,
    )
    batch_id = serializers.PrimaryKeyRelatedField(
        source="batch",
        queryset=CleaningBatch.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    host = serializers.PrimaryKeyRelatedField(read_only=True)
    assignment = AssignmentSerializer(read_only=True)

    class Meta:
        model = CleaningJob
        fields = [
            "id",
            "property_id",
            "property",
            "host",
            "batch_id",
            "batch",
            "title",
            "description",
            "scheduled_start",
            "scheduled_end",
            "currency",
            "proposed_price",
            "agreed_price",
            "status",
            "cleaning_instructions",
            "assignment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "property",
            "host",
            "batch",
            "agreed_price",
            "status",
            "assignment",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        scheduled_start = attrs.get("scheduled_start", getattr(self.instance, "scheduled_start", None))
        scheduled_end = attrs.get("scheduled_end", getattr(self.instance, "scheduled_end", None))
        if scheduled_start and scheduled_end and scheduled_end <= scheduled_start:
            raise serializers.ValidationError("scheduled_end must be after scheduled_start.")
        return attrs


class CleanerApplicationSerializer(serializers.ModelSerializer):
    job_id = serializers.PrimaryKeyRelatedField(
        source="job",
        queryset=CleaningJob.objects.all(),
        write_only=True,
    )
    cleaner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CleanerApplication
        fields = [
            "id",
            "job_id",
            "job",
            "cleaner",
            "status",
            "proposed_price",
            "message",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "job", "cleaner", "status", "created_at", "updated_at"]

