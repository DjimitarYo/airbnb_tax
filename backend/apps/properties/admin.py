from django.contrib import admin

from apps.properties.models import ExternalCalendarConnection, Property, Reservation


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "host", "default_cleaning_duration_minutes", "default_price_eur")
    list_filter = ("city", "country")
    search_fields = ("name", "address", "city", "host__username")


@admin.register(ExternalCalendarConnection)
class ExternalCalendarConnectionAdmin(admin.ModelAdmin):
    list_display = ("name", "property", "provider", "direction", "status", "last_sync_at")
    list_filter = ("provider", "direction", "status")
    search_fields = ("name", "property__name", "feed_url", "external_calendar_id")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("property", "source", "guest_name", "starts_at", "ends_at")
    list_filter = ("source",)
    search_fields = ("property__name", "guest_name", "external_uid")

