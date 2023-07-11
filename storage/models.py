import uuid

from django.utils import timezone
from django.db import models
# https://docs.djangoproject.com/en/4.2/ref/validators/ - validators docs
from django.core.validators import MinValueValidator


class Storage(models.Model):
    location = models.CharField(max_length=200, blank=False, null=False)
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    capacity = models.IntegerField(validators=[MinValueValidator(1)], null=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return f"{self.name}, {self.location}"


class Truck(models.Model):
    truck_id = models.UUIDField(unique=True, default=uuid.uuid4, blank=False, null=False)
    capacity = models.IntegerField(validators=[MinValueValidator(1)], blank=False, null=False)
    current_storage = models.ForeignKey(Storage, on_delete=models.SET_NULL, null=True)
    exploitation_start = models.DateTimeField(blank=False, null=False)
    # expluatation_finish - datetime > expluatation_start
    exploitation_finish = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return f"{self.truck_id}, {self.exploitation_start}, storage:{self.current_storage}"
