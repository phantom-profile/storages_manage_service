from django import forms

from lib.users_services import CurrencyConverter


class ConvertorForm(forms.Form):
    convert_from = forms.ChoiceField(label='From', choices=CurrencyConverter.CHOICES)
    convert_to = forms.ChoiceField(label='To', choices=CurrencyConverter.CHOICES)
    amount_from = forms.FloatField(label='Amount', initial=0, min_value=0)
    amount_to = forms.FloatField(label='Result', initial=0, min_value=0, disabled=True)
