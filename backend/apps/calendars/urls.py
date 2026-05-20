from django.urls import path

from apps.calendars.views import CalendarConflictView


urlpatterns = [
    path("conflicts/", CalendarConflictView.as_view(), name="calendar-conflicts"),
]

