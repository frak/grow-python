from django.db import models
from rest_framework import serializers

from grow_api.models import Channel, GrowUnit


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = (
            'number', 'plant', 'enabled', 'auto_water', 'alarm', 'wet_point', 'dry_point', 'alarm_point', 'pump_speed',
            'pump_duration'
        )


class GrowUnitSerializer(serializers.ModelSerializer):
    channels = ChannelSerializer(many=True)
    joined_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = GrowUnit
        fields = (
            'host', 'title', 'description', 'wait_interval', 'channels', 'joined_at'
        )
        constraints = [
            models.UniqueConstraint(fields=['host'], name='UNIQUE_HOST'),
            models.UniqueConstraint(fields=['title'], name='UNIQUE_TITLE'),
        ]
