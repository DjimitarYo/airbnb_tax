from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.accounts.models import CleanerProfile, HostProfile


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "preferred_language",
            "role",
            "password",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()

        if user.is_host:
            HostProfile.objects.get_or_create(user=user)
        elif user.is_cleaner:
            CleanerProfile.objects.get_or_create(user=user)

        return user


class HostProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = HostProfile
        fields = ["id", "user", "company_name", "city", "notes", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class CleanerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = CleanerProfile
        fields = [
            "id",
            "user",
            "kind",
            "verification_status",
            "display_name",
            "bio",
            "service_areas",
            "average_rating",
            "completed_jobs_count",
            "is_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "average_rating",
            "completed_jobs_count",
            "is_verified",
            "created_at",
            "updated_at",
        ]

