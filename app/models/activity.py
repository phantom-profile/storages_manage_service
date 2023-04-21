from pydantic import BaseModel, PositiveInt, NonNegativeInt
from datetime import datetime


class Activity(BaseModel):
    id: PositiveInt
    title: str
    start_time: datetime


class ActivityList(BaseModel):
    activities: list[Activity]
    count: NonNegativeInt
