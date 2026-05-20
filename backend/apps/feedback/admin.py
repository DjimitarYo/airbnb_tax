from django.contrib import admin

from apps.feedback.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("job", "reviewer", "reviewee", "rating", "is_private_issue", "created_at")
    list_filter = ("rating", "is_private_issue")
    search_fields = ("job__title", "reviewer__username", "reviewee__username", "comment")

