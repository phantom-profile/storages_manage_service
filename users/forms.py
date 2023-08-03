from django import forms
from django.forms import ModelForm

from lib.users_services import CurrencyConverter
from users.models import CreditCard


class ConvertorForm(forms.Form):
    convert_from = forms.ChoiceField(label='From', choices=CurrencyConverter.CHOICES)
    convert_to = forms.ChoiceField(label='To', choices=CurrencyConverter.CHOICES)
    amount_from = forms.FloatField(label='Amount', initial=0, min_value=0)
    amount_to = forms.FloatField(label='Result', initial=0, min_value=0, disabled=True)


class CreditCardForm(ModelForm):
    class Meta:
        model = CreditCard
        fields = ['card_number', 'cvv', 'owner', 'bank', 'vendor', 'expires_at']
        widgets = {
            'expires_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': "datetime-local"}),
        }
