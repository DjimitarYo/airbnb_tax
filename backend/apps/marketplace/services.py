from __future__ import annotations

from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.accounts.models import CleanerProfile, User
from apps.marketplace.models import Assignment, CleanerApplication, CleaningJob
from apps.notifications.services import create_notification


class MarketplaceError(ValueError):
    pass


def publish_job(job: CleaningJob) -> CleaningJob:
    if job.status != CleaningJob.Status.DRAFT:
        raise MarketplaceError("Only draft jobs can be published.")
    job.status = CleaningJob.Status.OPEN
    job.save(update_fields=["status", "updated_at"])
    return job


def submit_application(
    *,
    job: CleaningJob,
    cleaner: User,
    proposed_price: Decimal | None = None,
    message: str = "",
) -> CleanerApplication:
    if not cleaner.is_cleaner:
        raise MarketplaceError("Only cleaners can apply for cleaning jobs.")

    try:
        cleaner_profile = cleaner.cleaner_profile
    except CleanerProfile.DoesNotExist as exc:
        raise MarketplaceError("Cleaner profile is required before applying.") from exc

    if not cleaner_profile.is_verified:
        raise MarketplaceError("Cleaner must be verified before applying.")

    if job.status != CleaningJob.Status.OPEN:
        raise MarketplaceError("Cleaner can apply only to open jobs.")

    application, created = CleanerApplication.objects.get_or_create(
        job=job,
        cleaner=cleaner,
        defaults={"proposed_price": proposed_price, "message": message},
    )
    if not created and application.status == CleanerApplication.Status.WITHDRAWN:
        application.status = CleanerApplication.Status.PENDING
        application.proposed_price = proposed_price
        application.message = message
        application.save(update_fields=["status", "proposed_price", "message", "updated_at"])
    elif not created:
        raise MarketplaceError("Cleaner has already applied for this job.")

    create_notification(
        user=job.host,
        notification_type="application.submitted",
        title="New cleaner application",
        body=f"{cleaner.get_username()} applied for {job.title}.",
        metadata={"job_id": job.id, "application_id": application.id},
    )
    return application


@transaction.atomic
def accept_application(
    *,
    application: CleanerApplication,
    accepted_by: User,
    agreed_price: Decimal | None = None,
) -> Assignment:
    application = CleanerApplication.objects.select_for_update().select_related("job", "cleaner").get(
        id=application.id
    )
    job = CleaningJob.objects.select_for_update().get(id=application.job_id)

    if not (accepted_by.is_platform_admin or job.host_id == accepted_by.id):
        raise MarketplaceError("Only the host or admin can accept applications.")

    if job.status != CleaningJob.Status.OPEN:
        raise MarketplaceError("Applications can be accepted only for open jobs.")

    if hasattr(job, "assignment"):
        raise MarketplaceError("This job already has an assignment.")

    application.status = CleanerApplication.Status.ACCEPTED
    application.save(update_fields=["status", "updated_at"])

    CleanerApplication.objects.filter(job=job).exclude(id=application.id).update(
        status=CleanerApplication.Status.REJECTED,
        updated_at=timezone.now(),
    )

    assignment = Assignment.objects.create(
        job=job,
        cleaner=application.cleaner,
        application=application,
        agreed_price=agreed_price if agreed_price is not None else application.proposed_price,
    )

    job.status = CleaningJob.Status.ASSIGNED
    job.agreed_price = assignment.agreed_price
    job.save(update_fields=["status", "agreed_price", "updated_at"])

    create_notification(
        user=application.cleaner,
        notification_type="assignment.accepted",
        title="Cleaning job assigned",
        body=f"You were assigned to {job.title}.",
        metadata={"job_id": job.id, "assignment_id": assignment.id},
    )
    return assignment


@transaction.atomic
def complete_job(*, job: CleaningJob, completed_by: User) -> CleaningJob:
    job = CleaningJob.objects.select_for_update().get(id=job.id)

    if job.status != CleaningJob.Status.ASSIGNED:
        raise MarketplaceError("Only assigned jobs can be completed.")

    if not hasattr(job, "assignment"):
        raise MarketplaceError("Job cannot be completed without an assignment.")

    if not (
        completed_by.is_platform_admin
        or completed_by.id == job.host_id
        or completed_by.id == job.assignment.cleaner_id
    ):
        raise MarketplaceError("Only an involved user can complete this job.")

    assignment = job.assignment
    assignment.completed_at = timezone.now()
    assignment.save(update_fields=["completed_at", "updated_at"])

    job.status = CleaningJob.Status.COMPLETED
    job.save(update_fields=["status", "updated_at"])

    create_notification(
        user=job.host,
        notification_type="job.completed",
        title="Cleaning completed",
        body=f"{job.title} was marked completed.",
        metadata={"job_id": job.id},
    )
    create_notification(
        user=assignment.cleaner,
        notification_type="review.requested",
        title="Leave feedback",
        body=f"Please review your experience for {job.title}.",
        metadata={"job_id": job.id},
    )
    return job

