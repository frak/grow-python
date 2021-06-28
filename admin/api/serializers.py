from django.db import models
from rest_framework import serializers

from .models import Channel, GrowUnit


class ChannelSerializer(serializers.ModelSerializer):
    grow_unit_id = serializers.PrimaryKeyRelatedField(queryset=GrowUnit.objects.all(), source='grow_unit.id')

    class Meta:
        model = Channel
        fields = (
            'number', 'plant', 'enabled', 'auto_water', 'alarm', 'wet_point', 'dry_point', 'alarm_point', 'pump_speed',
            'pump_duration', 'grow_unit_id'
        )


class GrowUnitSerializer(serializers.ModelSerializer):
    channels = ChannelSerializer(many=True, read_only=True)
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
