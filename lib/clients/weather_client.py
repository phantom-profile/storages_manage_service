from datetime import datetime

from requests import get

from lib.clients.base_client import BaseClient
from storages_manage_service.settings import env_variables


# docs - https://www.weatherapi.com/docs/
class WeatherApiClient(BaseClient):
    TOKEN = env_variables.get('WEATHER_API_TOKEN')
    URL = 'https://api.weatherapi.com/v1'
    FOUR_HOURS = 4 * 60 * 60

    def __init__(self, location: str, date: datetime = None, options: dict = None):
        super().__init__()
        self.location = location.strip().lower()
        self.date = date or datetime.now()
        self.options = options or {}

        self.cacher.set_key(self._redis_key)

    def current(self):
        if self.cacher.is_exist():
            return self.cacher.get_cached()

        self._response = get(
            url=self._build_url('current', request_format='json'),
            params={
                'q': self.location,
                'lang': self.options.get('lang', 'en'),
                'key': self.TOKEN
            }
        )

        self.cacher.save(self._service_response, time=self.FOUR_HOURS)
        return self._service_response

    @property
    def _redis_key(self):
        options_as_string = ''.join(self.options.values())
        return f'weather_api:{self.date.strftime("%m-%d-%Y")}:{self.location}:{options_as_string}'
