from django.db import models


class GrowUnit(models.Model):
    host = models.CharField(max_length=64, null=True, blank=True)
    title = models.CharField(max_length=64, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    wait_interval = models.IntegerField(null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class Channel(models.Model):
    number = models.IntegerField()
    plant = models.CharField(max_length=255, null=True, blank=True)
    enabled = models.BooleanField(default=False)
    auto_water = models.BooleanField(default=True)
    alarm = models.BooleanField(default=False)

    grow_unit = models.ForeignKey(GrowUnit, on_delete=models.CASCADE, related_name='channels')

    wet_point = models.DecimalField(decimal_places=1, max_digits=3)
    dry_point = models.DecimalField(decimal_places=1, max_digits=3)
    alarm_point = models.DecimalField(decimal_places=1, max_digits=3)

    pump_speed = models.DecimalField(decimal_places=1, max_digits=3)
    pump_duration = models.DecimalField(decimal_places=1, max_digits=3)

    def __str__(self):
        return f"{self.number} - {self.plant}" if len(self.plant) > 0 else f"{self.number}"

    class Meta:
        unique_together = ['grow_unit', 'number']
        ordering = ['number']
