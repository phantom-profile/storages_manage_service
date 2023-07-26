from django import forms
from django.core.validators import MinValueValidator

from storage.models import Storage


class UniqueValidator:
    def __call__(self, name):
        if Storage.objects.filter(name=name).exists():
            raise forms.ValidationError('error: field name must be unique')


class StorageForm(forms.Form):
    name = forms.CharField(
        label='Storage name',
        max_length=100,
        validators=[UniqueValidator()],
        help_text='Must be uniq in our system'
    )
    location = forms.CharField(
        label='Storage location',
        max_length=100,
        help_text='City, street, etc...'
    )
    capacity = forms.IntegerField(
        label='Storage capacity',
        validators=[MinValueValidator(1)],
        help_text='Counted in cubic meters'
    )


class FilterStoragesForm(forms.Form):
    ORDER_FIELDS = (
        ('id', 'Id'),
        ('name', 'Name'),
        ('location', 'Location'),
        ('capacity', 'Capacity'),
        ('trucks_count', 'Trucks available')
    )
    ORDERS_MAP = {
        False: '',
        True: '-'
    }
    SEARCH_PARAMS = {'name__contains', 'location__contains', 'capacity__gte'}

    name__contains = forms.CharField(label='Name contains', required=False)
    location__contains = forms.CharField(label='Location contains', required=False)
    capacity__gte = forms.IntegerField(
        label='Capacity greater than',
        help_text='Counted in cubic meters',
        required=False
    )
    sort_by = forms.CharField(label='Sort by', widget=forms.Select(choices=ORDER_FIELDS))
    reverse_order = forms.BooleanField(label='Reverse order', required=False, initial=True)

    @property
    def sort_string(self) -> str:
        if not self.data:
            return "-id"
        reverse = self.ORDERS_MAP[self.cleaned_data['reverse_order']]
        return f"{reverse}{self.cleaned_data['sort_by']}"

    @property
    def search_params(self) -> dict:
        if not self.data:
            return {}

        params = {
            'name__contains': self.cleaned_data['name__contains'],
            'location__contains': self.cleaned_data['location__contains'],
            'capacity__gte': self.cleaned_data['capacity__gte']
        }
        return {key: value for key, value in params.items() if value}
