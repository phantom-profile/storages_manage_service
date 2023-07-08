from django.db import models


class Storage(models.Model):
    location = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    capacity = models.IntegerField(default=0)
    created_at = models.DateTimeField()