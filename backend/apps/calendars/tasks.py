try:
    from celery import shared_task
except ImportError:  # pragma: no cover - lets local syntax checks pass before deps install.
    def shared_task(func=None, **_kwargs):
        if func is None:
            return lambda wrapped: wrapped
        return func


@shared_task
def sync_ical_connection(connection_id: int) -> int:
    # Actual iCal parsing will be added once external feed behavior is finalized.
    return connection_id


@shared_task
def sync_google_calendar(connection_id: int) -> int:
    # Google OAuth and Calendar API integration are intentionally deferred.
    return connection_id

