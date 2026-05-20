from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import CleanerProfile, HostProfile, User


@admin.register(User)
class AppUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Marketplace", {"fields": ("role", "phone_number", "preferred_language")}),
    )
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = UserAdmin.list_filter + ("role",)


@admin.register(HostProfile)
class HostProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "company_name", "city", "created_at")
    search_fields = ("user__username", "company_name", "city")


@admin.register(CleanerProfile)
class CleanerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "display_name",
        "kind",
        "verification_status",
        "average_rating",
        "completed_jobs_count",
    )
    list_filter = ("kind", "verification_status")
    search_fields = ("user__username", "display_name", "service_areas")

