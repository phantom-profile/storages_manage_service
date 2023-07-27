from typing import Iterable

from django.db.models import Count

from storage.forms import FilterStoragesForm
from storage.models import Storage


class GetStoragesService:
    def __init__(self, form: FilterStoragesForm):
        form.is_valid()

        self.search_params = form.search_params
        self.order = form.sort_string

    @property
    def list(self) -> Iterable[Storage]:
        storages = Storage.objects.all().annotate(trucks_count=Count('truck'))
        if self.search_params:
            storages = storages.filter(**self.search_params)
        return storages.order_by(self.order)
