from datetime import datetime

from requests import get

from lib.clients.base_client import BaseClient
from storages_manage_service.settings import env_variables


# docs - https://currencyapi.com/docs
class CurrenciesApiClient(BaseClient):
    URL = 'https://api.currencyapi.com/v3'
    TOKEN = env_variables.get('CURRENCIES_API_TOKEN')
    TEN_HOURS = 10 * 60 * 60
    DEFAULT = ['USD', 'EUR', 'KZT', 'RUB', 'BTC']

    def __init__(self, convert_from: str, convert_to: str):
        super().__init__()
        self.convert_from = convert_from
        self.convert_to = convert_to

        self.cacher.set_key(self.redis_key)

    def status(self):
        self._response = get(
            url=self._build_url("status"),
            params={'apikey': self.TOKEN}
        )
        return self._service_response

    def get_currency(self):
        if self.cacher.is_exist():
            cache = self.cacher.get_cached()
            data = cache['response_body'].get('data', {})
            if self.convert_to in data:
                return cache

        self._response = get(
            url=self._build_url("latest"),
            params={
                'apikey': self.TOKEN,
                'base_currency': self.convert_from,
                'currencies': ','.join([self.convert_to] + self.DEFAULT)
            }
        )

        if self._is_successful:
            self.cacher.save(self._service_response, time=self.TEN_HOURS)
        return self._service_response

    @property
    def redis_key(self):
        return f'currency_api:{datetime.now().strftime("%m-%d-%Y")}:{self.convert_from}'
