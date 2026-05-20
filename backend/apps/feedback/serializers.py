from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.feedback.models import Review
from apps.marketplace.models import CleaningJob


User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    job_id = serializers.PrimaryKeyRelatedField(
        source="job",
        queryset=CleaningJob.objects.all(),
        write_only=True,
    )
    reviewee_id = serializers.PrimaryKeyRelatedField(
        source="reviewee",
        queryset=User.objects.all(),
        write_only=True,
    )
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "job_id",
            "job",
            "reviewer",
            "reviewee_id",
            "reviewee",
            "rating",
            "comment",
            "private_note",
            "is_private_issue",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "job", "reviewer", "reviewee", "created_at", "updated_at"]

