from json import loads, dumps
from typing import Optional

from requests import Response, exceptions

from lib.redis_client import Red


class CacheService:
    def __init__(self):
        self.__key = None

    @property
    def key(self):
        if not self.__key:
            raise NotImplementedError('add key through .set_key("my-key")')
        return self.__key

    def set_key(self, key: str):
        self.__key = key

    def is_exist(self):
        return Red.exists(self.key)

    def get_cached(self):
        if not self.is_exist():
            return None
        return loads(Red.get(self.key))

    def save(self, jsonable: dict, time: int = None):
        if time:
            Red.setex(self.key, time, dumps(jsonable))
            return
        Red.set(self.key, dumps(jsonable))


class BaseClient:
    URL = ''
    TOKEN = ''

    def __init__(self):
        if not self.TOKEN:
            raise AttributeError('Weather API token is empty! Add it to .env config')

        self._response: Optional[Response] = None
        self.cacher = CacheService()

    # FOR INTERNAL USAGE ONLY
    @property
    def _service_response(self):
        return {
            'status': self._response.status_code,
            'requested_url': self._response.url,
            'is_successful': self._is_successful,
            'response_body': self._parsed_response
        }

    def _build_url(self, path: str, request_format: str = None):
        if not request_format:
            return f'{self.URL}/{path}'
        return f'{self.URL}/{path}.{request_format}'

    @property
    def _is_successful(self):
        return 200 <= self._response.status_code < 300

    @property
    def _parsed_response(self):
        try:
            return self._response.json()
        except exceptions.JSONDecodeError:
            return {"error": "impossible to decode to JSON", "original_text": self._response.text}
