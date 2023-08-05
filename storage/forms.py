from django import forms
from storage.models import Storage


class StorageForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = ("name", "location", "capacity")


class FilterStoragesForm(forms.Form):
    ORDER_FIELDS = (
        ('id', 'Id'),
        ('name', 'Name'),
        ('location', 'Location'),
        ('capacity', 'Capacity'),
        ('current_load', 'Current load'),
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
        if not self.data_presents('reverse_order', 'sort_by'):
            return "-id"
        reverse = self.ORDERS_MAP[self.cleaned_data['reverse_order']]
        return f"{reverse}{self.cleaned_data['sort_by']}"

    @property
    def search_params(self) -> dict:
        if not self.data_presents('name__contains', 'location__contains', 'capacity__gte'):
            return {}

        params = {
            'name__contains': self.cleaned_data['name__contains'],
            'location__contains': self.cleaned_data['location__contains'],
            'capacity__gte': self.cleaned_data['capacity__gte']
        }
        return {key: value for key, value in params.items() if value}

    def data_presents(self, *keys):
        for key in keys:
            if key not in self.data:
                return False
        return True
