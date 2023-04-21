from pydantic import BaseModel, PositiveInt, NonNegativeInt
from datetime import datetime


class BaseActivity(BaseModel):
    title: str
    start_time: datetime


class Activity(BaseActivity):
    id: PositiveInt


class ActivityList(BaseModel):
    activities: list[Activity]
    count: NonNegativeInt
