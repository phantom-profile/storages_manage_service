from django import forms
from django.core.validators import MinValueValidator

from storage.models import Storage


class UniqueValidator:
    def __call__(self, name):
        if Storage.objects.filter(name=name).exists():
            raise forms.ValidationError('error: field name must be unique')


class StorageForm(forms.Form):

    location = forms.CharField(
        label='Storage location',
        max_length=100,
        help_text='City, street, etc...'
    )
    name = forms.CharField(
        label='Storage name',
        max_length=100,
        validators=[UniqueValidator()],
        help_text='Must be uniq in our system'
    )
    capacity = forms.IntegerField(
        label='Storage capacity',
        validators=[MinValueValidator(1)],
        help_text='Counted in cubic meters'
    )
