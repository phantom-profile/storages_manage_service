from pydantic import BaseModel, PositiveInt, NonNegativeInt, Field, validator
from datetime import datetime
from enum import StrEnum, auto


class OrderEnum(StrEnum):
    DESC = auto()
    ASC = auto()


class BaseActivity(BaseModel):
    title: str = Field(..., min_length=1)
    start_time: datetime
    is_done: bool = False
    description: str = ''


class Activity(BaseActivity):
    id: PositiveInt


class UpdateActivity(BaseModel):
    title: str | None
    start_time: datetime | None
    is_done: bool | None
    description: str | None

    @validator('title')
    def prevent_none(cls, title):
        if title is not None:
            assert len(title) > 0, 'title must present'
        return title


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


class ActivityWithMessage(BaseModel):
    activity: Activity | BaseActivity
    message: str = 'success'
