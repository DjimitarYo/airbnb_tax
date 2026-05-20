from django.contrib import admin

from apps.marketplace.models import Assignment, CleanerApplication, CleaningBatch, CleaningJob


@admin.register(CleaningBatch)
class CleaningBatchAdmin(admin.ModelAdmin):
    list_display = ("title", "property", "host", "month", "status")
    list_filter = ("status", "month")
    search_fields = ("title", "property__name", "host__username")


@admin.register(CleaningJob)
class CleaningJobAdmin(admin.ModelAdmin):
    list_display = ("title", "property", "host", "scheduled_start", "status", "proposed_price", "agreed_price")
    list_filter = ("status", "currency", "property__city")
    search_fields = ("title", "property__name", "host__username")


@admin.register(CleanerApplication)
class CleanerApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "cleaner", "status", "proposed_price", "created_at")
    list_filter = ("status",)
    search_fields = ("job__title", "cleaner__username")


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("job", "cleaner", "agreed_price", "assigned_at", "completed_at", "cancelled_at")
    search_fields = ("job__title", "cleaner__username")

