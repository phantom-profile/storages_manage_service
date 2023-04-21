import datetime
import random

from fastapi import FastAPI
from app.models.activity import ActivityList
from app.services.get_activities_service import GetActivitiesService
from app.queries.create_activity_query import CreateActivityQuery

app = FastAPI()


@app.get('/')
def main_page():
    return {'hello': 'world'}


@app.get('/activities')
def activities_list(query: str | None = None) -> ActivityList:
    activities = GetActivitiesService(query).perform()
    return ActivityList(activities=activities, count=len(activities))


# wwrong implementation just mock to easy data generate
# TODO: remove
@app.get('/make')
def create_activity() -> dict:
    attributes = {'title': 'hello', 'start_time': datetime.datetime(2023, 3, random.randint(1, 31))}
    new = CreateActivityQuery(attributes)
    new.execute()
    return {'result': new.is_successful, 'error': new.error_message}
