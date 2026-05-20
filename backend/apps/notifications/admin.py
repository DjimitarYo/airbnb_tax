from django.contrib import admin

from apps.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "notification_type", "channel", "title", "read_at", "sent_at", "created_at")
    list_filter = ("notification_type", "channel", "read_at", "sent_at")
    search_fields = ("user__username", "title", "body")

