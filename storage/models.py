from django.utils import timezone
from django.db import models
# https://docs.djangoproject.com/en/4.2/ref/validators/ - validators docs
from django.core.validators import MinValueValidator


class Storage(models.Model):
    location = models.CharField(max_length=200, blank=False, null=False)
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    capacity = models.IntegerField(validators=[MinValueValidator(1)], null=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)


# model Truck
# truck_id - unique string, uuid models.UUIDField with default call python uuid.uuid4
# capacity - integer > 0
# current_storage - 1toM relation with storage. One storage - many trucks. check models.ForeignKey
# expluatation_start - datetime
# expluatation_finish - datetime > expluatation_start
# created_at - datetime, default = timezone.now
