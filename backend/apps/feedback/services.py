from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models import Avg

from apps.accounts.models import CleanerProfile
from apps.feedback.models import Review
from apps.marketplace.models import CleaningJob
from apps.notifications.services import create_notification


User = get_user_model()


class FeedbackError(ValueError):
    pass


def submit_review(
    *,
    job: CleaningJob,
    reviewer: User,
    reviewee: User,
    rating: int,
    comment: str = "",
    private_note: str = "",
    is_private_issue: bool = False,
) -> Review:
    if job.status != CleaningJob.Status.COMPLETED:
        raise FeedbackError("Reviews are allowed only after job completion.")

    if not hasattr(job, "assignment"):
        raise FeedbackError("Reviewed job must have an assignment.")

    involved_user_ids = {job.host_id, job.assignment.cleaner_id}
    if reviewer.id not in involved_user_ids or reviewee.id not in involved_user_ids:
        raise FeedbackError("Only users involved in the job can review each other.")

    if reviewer.id == reviewee.id:
        raise FeedbackError("Users cannot review themselves.")

    review = Review.objects.create(
        job=job,
        reviewer=reviewer,
        reviewee=reviewee,
        rating=rating,
        comment=comment,
        private_note=private_note,
        is_private_issue=is_private_issue,
    )
    refresh_cleaner_rating(reviewee)
    create_notification(
        user=reviewee,
        notification_type="review.submitted",
        title="New review received",
        body=f"You received feedback for {job.title}.",
        metadata={"job_id": job.id, "review_id": review.id},
    )
    return review


def refresh_cleaner_rating(user: User) -> None:
    if not user.is_cleaner:
        return
    try:
        profile = user.cleaner_profile
    except CleanerProfile.DoesNotExist:
        return

    aggregate = Review.objects.filter(reviewee=user).aggregate(average=Avg("rating"))
    completed_count = user.cleaning_assignments.filter(job__status=CleaningJob.Status.COMPLETED).count()
    profile.average_rating = aggregate["average"] or 0
    profile.completed_jobs_count = completed_count
    profile.save(update_fields=["average_rating", "completed_jobs_count", "updated_at"])

