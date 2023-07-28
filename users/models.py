from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone


class CreditCard(models.Model):
    card_number = models.CharField(validators=[MinLengthValidator], max_length=16, blank=False, null=False)
    cvv = models.CharField(max_length=3, blank=False, null=False)
    owner = models.CharField(max_length=50, blank=False, null=False)
    expires_at = models.DateTimeField(blank=False, null=False)
    vendor = models.CharField(max_length=4, blank=False, null=False)
    bank = models.CharField(max_length=50, blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"card number - {self.card_number},cvv - {self.cvv}, owner - {self.owner}"


User = get_user_model()
