from pydantic import BaseModel, PositiveInt
from datetime import datetime


class Activity(BaseModel):
    id: PositiveInt
    title: str
    start_time: datetime
