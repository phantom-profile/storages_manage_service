from fastapi import FastAPI, Depends, HTTPException
from pydantic import PositiveInt

from app.models.activity import (
    Activity, ActivityList, BaseActivity, ActivitiesFilter, ActivityWithMessage, UpdateActivity
)

from app.services.create_activity_service import CreateActivityService
from app.services.delete_ativity_service import DeleteActivityService
from app.services.get_activities_service import GetActivitiesService, GetActivityService
from app.services.update_activity_service import UpdateActivityService

app = FastAPI()


@app.get('/')
def main_page():
    return {
        'activities manage api': 'made by phantome-profile',
        'documentation': '/docs'
    }


@app.get('/activities')
def activities_list(query: ActivitiesFilter = Depends()) -> ActivityList:
    activities = GetActivitiesService(query).perform()
    return ActivityList(activities=activities, count=len(activities))


@app.get('/activities/{id}')
def get_activity(activity_id: PositiveInt) -> Activity:
    activity = GetActivityService(activity_id=activity_id).perform()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@app.post('/activities')
def create_activity(activity: BaseActivity) -> ActivityWithMessage:
    service_result = CreateActivityService(activity=activity).perform()
    return service_result


@app.patch('/activities/{id}')
def update_activity(activity_id: PositiveInt, activity: UpdateActivity) -> ActivityWithMessage:
    service_result = UpdateActivityService(activity_id=activity_id, activity=activity).perform()
    if not service_result:
        raise HTTPException(status_code=404, detail="Activity not found")
    return service_result


@app.delete('/activities/{id}')
def delete_activity(activity_id: PositiveInt) -> ActivityWithMessage:
    service_result = DeleteActivityService(activity_id=activity_id).perform()
    if not service_result:
        raise HTTPException(status_code=404, detail="Activity not found")
    return service_result
