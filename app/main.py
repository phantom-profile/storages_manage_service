from fastapi import FastAPI, Depends, HTTPException
from pydantic import PositiveInt

from app.models.activity import Activity, ActivityList, BaseActivity, ActivitiesFilter
from app.services.get_activities_service import GetActivitiesService
from app.queries.create_activity_query import CreateActivityQuery

app = FastAPI()


@app.get('/')
def main_page():
    return {'hello': 'world'}


@app.get('/activities')
def activities_list(query: ActivitiesFilter = Depends()) -> ActivityList:
    activities = GetActivitiesService(query).perform()
    return ActivityList(activities=activities, count=len(activities))


@app.get('/activities/{id}')
def get_activity(activity_id: PositiveInt) -> Activity:
    query = ActivitiesFilter(id=activity_id, per_page=1)
    result = GetActivitiesService(query).perform()
    if not result:
        raise HTTPException(status_code=404, detail="Activity not found")
    return result[0]


@app.post('/activities')
def create_activity(activity: BaseActivity) -> dict:
    new = CreateActivityQuery(activity.dict())
    new.execute()
    return {'result': new.is_successful, 'error': new.error_message}
