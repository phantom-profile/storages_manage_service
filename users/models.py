from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


def validation_vendor(vendor):
    vendors = ["VISA", "MC", "MIR"]
    if vendor not in vendors:
        raise ValidationError("Invalid input. Valid values: %(vendors)", params={"vendors": vendors})


class CreditCard(models.Model):
    card_number = models.CharField(max_length=16, blank=False, null=False)
    cvv = models.CharField(max_length=3, blank=False, null=False)
    owner = models.CharField(max_length=50, blank=False, null=False)
    expires_at = models.DateTimeField(blank=True, null=True)
    vendor = models.CharField(max_length=4, validators=[validation_vendor])
    bank = models.CharField(max_length=50, blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now)


User = get_user_model()
q = CreditCard(card_number = 12, cvv ="SDF", owner="asd",vendor="MIR",bank="asd")
