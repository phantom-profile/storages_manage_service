from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


def valid_cvv(cvv):
    if not cvv.isdigit() or len(cvv) != 3:
        raise ValidationError("INVALID CVV")


def valid_card_number(card_number):
    if not card_number.isdigit() or len(card_number) != 16:
        raise ValidationError("INVALID CARD NUMBER")


class CreditCard(models.Model):
    VENDORS = (
        ("VISA", "VISA"),
        ("MIR", "MIR"),
        ("MASTER CARD", "MASTER CARD"),
        ("MAESTRO", "MAESTRO")
    )
    BANKS = (
        ("Sber", "Sber"),
        ("Tinkoff", "Tinkoff"),
        ("Kaspi", "Kaspi"),
        ("Gazprom", "Gazprom"),
        ("Unicredit", "Unicredit")
    )

    card_number = models.CharField(validators=[valid_card_number],
                                   max_length=16, blank=False, null=False)
    cvv = models.CharField(validators=[valid_cvv], max_length=3, blank=False, null=False)
    owner = models.CharField(max_length=60, blank=False, null=False)
    expires_at = models.DateTimeField(blank=False, null=False)
    vendor = models.CharField(choices=VENDORS, max_length=11, blank=False, null=False)
    bank = models.CharField(choices=BANKS, max_length=9, blank=False, null=False)
    card_uuid = models.UUIDField(blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"card number - {self.card_number},cvv - {self.cvv}, owner - {self.owner}"


User = get_user_model()
