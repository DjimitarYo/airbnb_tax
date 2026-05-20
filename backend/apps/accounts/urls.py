from rest_framework.routers import DefaultRouter

from apps.accounts.views import CleanerProfileViewSet, HostProfileViewSet, UserViewSet


router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("hosts", HostProfileViewSet, basename="host-profile")
router.register("cleaners", CleanerProfileViewSet, basename="cleaner-profile")

urlpatterns = router.urls

