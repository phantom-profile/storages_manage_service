from django import forms
from storage.models import Storage


class UniqueValidator():
    def __call__(self, name):
        if Storage.objects.filter(name=name):
            raise forms.ValidationError('ошибка')


class StorageForm(forms.Form):
    location = forms.CharField(label='Storage location', max_length=100)
    name = forms.CharField(label='Storage name', max_length=100, validators=[UniqueValidator()])
    capacity = forms.IntegerField(label='Storage capacity')


