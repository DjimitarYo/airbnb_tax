from rest_framework.routers import DefaultRouter

from apps.properties.views import (
    ExternalCalendarConnectionViewSet,
    PropertyViewSet,
    ReservationViewSet,
)


router = DefaultRouter()
router.register("properties", PropertyViewSet, basename="property")
router.register("calendar-connections", ExternalCalendarConnectionViewSet, basename="calendar-connection")
router.register("reservations", ReservationViewSet, basename="reservation")

urlpatterns = router.urls

