from datetime import datetime
from json import dumps, loads
from typing import Optional

from requests import get, Response, exceptions

from lib.redis_client import Red
from storages_manage_service.settings import env_variables


# docs - https://www.weatherapi.com/docs/
class WeatherService:
    URL = 'https://api.weatherapi.com/v1'
    TOKEN = env_variables.get('WEATHER_API_TOKEN')
    FOUR_HOURS = 4 * 60 * 60

    __slots__ = ('location', 'date', 'options', 'response')

    def __init__(self, location: str, date: datetime = None, options: dict = None):
        if not self.TOKEN:
            raise AttributeError('Weather API token is empty! Add it to .env config')

        self.location = location.strip().lower()
        self.date = date or datetime.now()
        self.options = options or {}
        self.response: Optional[Response] = None

    def current(self):
        if Red.exists(self.redis_key):
            return loads(Red.get(self.redis_key))

        self.response = get(
            url=self.build_url('current'),
            params={
                'q': self.location,
                'lang': self.options.get('lang', 'en'),
                'key': self.TOKEN
            }
        )

        if self.is_successful:
            Red.setex(self.redis_key, self.FOUR_HOURS, dumps(self.service_response))
        return self.service_response

    # PRIVATE METHODS SECTION

    @property
    def redis_key(self):
        options_as_string = ''.join(self.options.values())
        return f'weather_api:{self.date.strftime("%m-%d-%Y")}:{self.location}:{options_as_string}'

    @property
    def service_response(self):
        return {
            'status': self.response.status_code,
            'requested_url': self.response.url,
            'is_successful': self.is_successful,
            'response_body': self.parsed_response
        }

    def build_url(self, path: str):
        return f'{self.URL}/{path}.json'

    @property
    def is_successful(self):
        return 200 <= self.response.status_code < 300

    @property
    def parsed_response(self):
        try:
            return self.response.json()
        except exceptions.JSONDecodeError:
            return {"error": "impossible to decode to JSON", "original_text": self.response.text}
