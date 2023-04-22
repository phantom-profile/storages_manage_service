from pydantic import BaseModel, PositiveInt, NonNegativeInt
from datetime import datetime
from enum import StrEnum, auto


class OrderEnum(StrEnum):
    DESC = auto()
    ASC = auto()


class BaseActivity(BaseModel):
    title: str
    start_time: datetime


class Activity(BaseActivity):
    id: PositiveInt


class ActivityList(BaseModel):
    activities: list[Activity]
    count: NonNegativeInt


class ActivitiesFilter(BaseModel):
    id: PositiveInt | None
    title_like: str | None
    order: OrderEnum = OrderEnum.DESC
    page: PositiveInt = 1
    per_page: PositiveInt = 50
    sort_by: str | None
