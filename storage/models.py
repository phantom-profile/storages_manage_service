import uuid

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
# https://docs.djangoproject.com/en/4.2/ref/validators/ - validators docs
from django.core.validators import MinValueValidator


class Storage(models.Model):
    location = models.CharField(max_length=200, blank=False, null=False)
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    capacity = models.IntegerField(validators=[MinValueValidator(1)], null=False)
    current_load = models.IntegerField(validators=[MinValueValidator(0)], null=False, default=0)
    created_at = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return f"Storage(id={self.pk}, name={self.name}, location={self.location})"

    def _validate_capacity_load(self):
        if self.capacity < self.current_load:
            raise ValidationError("Load cannot be more then capacity.")

    def save(self, *args, **kwargs):
        self._validate_capacity_load()
        return super().save(*args, **kwargs)


class Truck(models.Model):
    truck_id = models.UUIDField(unique=True, default=uuid.uuid4, blank=False, null=False)
    capacity = models.IntegerField(validators=[MinValueValidator(1)], blank=False, null=False)
    current_storage = models.ForeignKey(Storage, on_delete=models.SET_NULL, null=True)
    exploitation_start = models.DateTimeField(blank=False, null=False)
    exploitation_finish = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return f"{self.truck_id}, {self.exploitation_start}, storage:{self.current_storage}"

    def _validate_start_end_dates(self):
        if self.exploitation_finish <= self.exploitation_start:
            raise ValidationError("Exploitation period was set incorrectly.")

    def save(self, *args, **kwargs):
        self._validate_start_end_dates()
        return super().save(*args, **kwargs)
