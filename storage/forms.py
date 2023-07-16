from django import forms


class StorageForm(forms.Form):
    location = forms.CharField(label='Storage location', max_length=100)
    name = forms.CharField(label='Storage name', max_length=100)
    capacity = forms.IntegerField(label='Storage capacity')