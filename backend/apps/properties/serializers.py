from rest_framework import serializers

from apps.properties.models import ExternalCalendarConnection, Property, Reservation


class PropertySerializer(serializers.ModelSerializer):
    host = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "host",
            "name",
            "address",
            "city",
            "country",
            "timezone",
            "access_notes",
            "cleaning_instructions",
            "default_cleaning_duration_minutes",
            "default_price_eur",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "host", "created_at", "updated_at"]


class ExternalCalendarConnectionSerializer(serializers.ModelSerializer):
    property_id = serializers.PrimaryKeyRelatedField(
        source="property",
        queryset=Property.objects.all(),
        write_only=True,
    )

    class Meta:
        model = ExternalCalendarConnection
        fields = [
            "id",
            "property_id",
            "property",
            "provider",
            "name",
            "direction",
            "feed_url",
            "external_calendar_id",
            "status",
            "last_sync_at",
            "last_error",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "property",
            "status",
            "last_sync_at",
            "last_error",
            "created_at",
            "updated_at",
        ]


class ReservationSerializer(serializers.ModelSerializer):
    property_id = serializers.PrimaryKeyRelatedField(
        source="property",
        queryset=Property.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Reservation
        fields = [
            "id",
            "property_id",
            "property",
            "source",
            "external_uid",
            "guest_name",
            "starts_at",
            "ends_at",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "property", "created_at", "updated_at"]

