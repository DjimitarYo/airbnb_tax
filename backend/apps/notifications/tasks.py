try:
    from celery import shared_task
except ImportError:  # pragma: no cover - lets local syntax checks pass before deps install.
    def shared_task(func=None, **_kwargs):
        if func is None:
            return lambda wrapped: wrapped
        return func


@shared_task
def dispatch_notification(notification_id: int) -> int:
    # Provider integration will be added when email/SMS vendors are selected.
    return notification_id

