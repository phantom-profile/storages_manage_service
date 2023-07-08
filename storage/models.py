from datetime import datetime

from django.db import models
# https://docs.djangoproject.com/en/4.2/ref/validators/ - validators docs
from django.core.validators import MinValueValidator


class Storage(models.Model):
    location = models.CharField(max_length=200, blank=False, null=False)
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    capacity = models.IntegerField(validators=[MinValueValidator(1)], null=False)
    created_at = models.DateTimeField(default=datetime.now, null=False)
