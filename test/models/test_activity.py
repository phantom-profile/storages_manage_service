import datetime
import unittest

from pydantic import ValidationError
from json import loads
from app.models.activity import Activity


class TestActivityModel(unittest.TestCase):
    def test_valid_creation(self):
        activity = Activity(id=1, title='hello', start_time='2022-01-01 00:00')

        self.assertEqual(
            activity.dict(),
            {'id': 1, 'title': 'hello', 'start_time': datetime.datetime(2022, 1, 1, 0, 0)}
        )

    def test_invalid_creation(self):
        try:
            errors = {}
            Activity(id=-10, title=None, start_time='invalid date')
        except ValidationError as error:
            errors = loads(error.json())
        self.assertEqual(len(errors), 3)
