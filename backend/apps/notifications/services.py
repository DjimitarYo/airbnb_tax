from __future__ import annotations

from django.contrib.auth import get_user_model

from apps.notifications.models import Notification


User = get_user_model()


def create_notification(
    *,
    user: User,
    notification_type: str,
    title: str,
    body: str = "",
    channel: str = Notification.Channel.IN_APP,
    metadata: dict | None = None,
) -> Notification:
    return Notification.objects.create(
        user=user,
        notification_type=notification_type,
        channel=channel,
        title=title,
        body=body,
        metadata=metadata or {},
    )

