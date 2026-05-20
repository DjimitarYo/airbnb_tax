from rest_framework import serializers

from apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "notification_type",
            "channel",
            "title",
            "body",
            "metadata",
            "read_at",
            "sent_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

