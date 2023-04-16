import datetime
import pytest

from pydantic import ValidationError
from app.models.activity import Activity


def test_creating_activity():
    activity = Activity(id=1, title='hello', start_time='2022-01-01 00:00')
    assert activity.dict() == {'id': 1, 'title': 'hello', 'start_time': datetime.datetime(2022, 1, 1, 0, 0)}


def test_invalid_activity():
    with pytest.raises(ValidationError):
        Activity(id=-10, title=None, start_time='invalid date')
