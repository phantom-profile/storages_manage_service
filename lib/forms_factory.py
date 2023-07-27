from json import dumps, loads
from uuid import uuid4

from lib.redis_client import Red
from storage.forms import StorageForm, FilterStoragesForm


class FormsFactory:
    FORMS = {
        'storage': StorageForm,
        'filter-storages': FilterStoragesForm
    }

    @classmethod
    def save_state(cls, state: dict) -> str:
        uuid = uuid4()
        Red.setex(str(uuid), 60, dumps(state))
        return str(uuid)

    @classmethod
    def restore_by_key(cls, key: str | None, form_type: str):
        form_class = cls.FORMS.get(form_type)
        if not form_class:
            raise AttributeError(f'form with type {form_type} not registered')
        if not key:
            return form_class()
        json_params = Red.get(key)
        if not json_params:
            return form_class()

        params = loads(json_params)
        form = form_class(params)
        form.is_valid()
        return form

    @classmethod
    def produce(cls, form_type: str, params: dict = None):
        form_class = cls.FORMS.get(form_type)
        if not form_class:
            raise AttributeError(f'form with type {form_type} not registered')
        if not params:
            return form_class()
        return form_class(params)
