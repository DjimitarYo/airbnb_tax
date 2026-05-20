from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.models import TimeStampedModel


class User(AbstractUser):
    class Role(models.TextChoices):
        HOST = "host", "Host"
        CLEANER = "cleaner", "Cleaner"
        ADMIN = "admin", "Admin"

    class Language(models.TextChoices):
        BULGARIAN = "bg", "Bulgarian"
        ENGLISH = "en", "English"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.HOST)
    phone_number = models.CharField(max_length=32, blank=True)
    preferred_language = models.CharField(
        max_length=8,
        choices=Language.choices,
        default=Language.BULGARIAN,
    )

    @property
    def is_host(self) -> bool:
        return self.role == self.Role.HOST

    @property
    def is_cleaner(self) -> bool:
        return self.role == self.Role.CLEANER

    @property
    def is_platform_admin(self) -> bool:
        return self.role == self.Role.ADMIN or self.is_staff


class HostProfile(TimeStampedModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="host_profile",
    )
    company_name = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.company_name or self.user.get_username()


class CleanerProfile(TimeStampedModel):
    class Kind(models.TextChoices):
        INDIVIDUAL = "individual", "Individual"
        AGENCY = "agency", "Agency"

    class VerificationStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        VERIFIED = "verified", "Verified"
        REJECTED = "rejected", "Rejected"
        SUSPENDED = "suspended", "Suspended"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cleaner_profile",
    )
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.INDIVIDUAL)
    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
    )
    display_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    service_areas = models.JSONField(default=list, blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    completed_jobs_count = models.PositiveIntegerField(default=0)

    @property
    def is_verified(self) -> bool:
        return self.verification_status == self.VerificationStatus.VERIFIED

    def __str__(self) -> str:
        return self.display_name or self.user.get_username()

