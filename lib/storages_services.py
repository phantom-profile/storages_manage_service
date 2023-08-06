from typing import Iterable

from django.db.models import Count

from lib.clients.weather_client import WeatherApiClient
from storage.forms import FilterStoragesForm
from storage.models import Storage

from lib.notificators import FlashNotifier


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


class GetWeatherService:
    DEFAULT_ERROR = 'Something went wrong. Try later'
    TEN_SECONDS = 10 * 1000

    def __init__(self, location: str, notifier: FlashNotifier):
        self._location = location
        self._notifier = notifier
        self._client = WeatherApiClient(location)
        self._result = None

    def perform(self) -> None:
        if not self._location:
            return self._notifier.error("No location provided.")

        self._result = self._client.current()
        if not self._result['is_successful']:
            return self._notifier.error(self._get_error_message())
        return self._notifier.info(self._build_message(), delay=self.TEN_SECONDS)

    def _get_error_message(self) -> str:
        value = self._result
        for key in ('response_body', 'error', 'message'):
            if key in value:
                value = value.get(key, {})
        return value or self.DEFAULT_ERROR

    def _build_message(self):
        data = self._get_weather_data()
        img = f'<img src="{data["icon"]}" width = "20" height = "20">'

        return f'Weather in {data["country"]}' \
               f' {data["city"]} at {data["upd"]}: ' \
               f'{img} t: {data["temp"]} C°, w: {data["wind"]} km / h'

    def _get_weather_data(self) -> dict:
        location_node = self._result['response_body']['location']
        current_node = self._result['response_body']['current']
        weather_data = {
            'country': location_node['country'],
            'city': location_node['name'],
            'upd': current_node['last_updated'],
            'icon': current_node['condition']['icon'],
            'temp': current_node['temp_c'],
            'wind': current_node['wind_kph']
        }

        return weather_data
