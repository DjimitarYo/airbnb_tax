from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from apps.accounts.models import CleanerProfile, HostProfile, User
from apps.feedback.services import submit_review
from apps.marketplace.models import Assignment, CleanerApplication, CleaningJob
from apps.marketplace.services import (
    MarketplaceError,
    accept_application,
    complete_job,
    publish_job,
    submit_application,
)
from apps.notifications.models import Notification
from apps.properties.models import Property


class MarketplaceServiceTests(TestCase):
    def setUp(self):
        self.host = User.objects.create_user(username="host", password="password123", role=User.Role.HOST)
        HostProfile.objects.create(user=self.host)
        self.cleaner = User.objects.create_user(
            username="cleaner",
            password="password123",
            role=User.Role.CLEANER,
        )
        CleanerProfile.objects.create(
            user=self.cleaner,
            verification_status=CleanerProfile.VerificationStatus.VERIFIED,
            display_name="Verified Cleaner",
        )
        self.property = Property.objects.create(
            host=self.host,
            name="Center Apartment",
            city="Sofia",
            cleaning_instructions="Change linens and restock basics.",
        )
        self.job = CleaningJob.objects.create(
            property=self.property,
            host=self.host,
            title="Turnover cleaning",
            scheduled_start=timezone.now() + timedelta(days=1),
            scheduled_end=timezone.now() + timedelta(days=1, hours=2),
            proposed_price=Decimal("45.00"),
        )

    def test_verified_cleaner_can_apply_and_host_can_accept(self):
        publish_job(self.job)

        application = submit_application(
            job=self.job,
            cleaner=self.cleaner,
            proposed_price=Decimal("50.00"),
            message="Available for this turnover.",
        )
        assignment = accept_application(
            application=application,
            accepted_by=self.host,
            agreed_price=Decimal("50.00"),
        )

        self.job.refresh_from_db()
        application.refresh_from_db()

        self.assertEqual(application.status, CleanerApplication.Status.ACCEPTED)
        self.assertEqual(self.job.status, CleaningJob.Status.ASSIGNED)
        self.assertEqual(assignment.cleaner, self.cleaner)
        self.assertEqual(Assignment.objects.count(), 1)
        self.assertEqual(Notification.objects.filter(user=self.cleaner).count(), 1)

    def test_unverified_cleaner_cannot_apply(self):
        unverified = User.objects.create_user(
            username="unverified",
            password="password123",
            role=User.Role.CLEANER,
        )
        CleanerProfile.objects.create(user=unverified)
        publish_job(self.job)

        with self.assertRaises(MarketplaceError):
            submit_application(job=self.job, cleaner=unverified)

    def test_completed_job_can_receive_two_way_review(self):
        publish_job(self.job)
        application = submit_application(job=self.job, cleaner=self.cleaner)
        accept_application(application=application, accepted_by=self.host)

        completed = complete_job(job=self.job, completed_by=self.host)
        review = submit_review(
            job=completed,
            reviewer=self.host,
            reviewee=self.cleaner,
            rating=5,
            comment="Reliable and on time.",
        )

        self.cleaner.cleaner_profile.refresh_from_db()
        self.assertEqual(completed.status, CleaningJob.Status.COMPLETED)
        self.assertEqual(review.rating, 5)
        self.assertEqual(self.cleaner.cleaner_profile.average_rating, 5)

