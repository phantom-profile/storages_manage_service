from fastapi import FastAPI, Depends, HTTPException
from pydantic import PositiveInt

from app.models.activity import Activity, ActivityList, BaseActivity, ActivitiesFilter, ActivityWithMessage
from app.services.get_activities_service import GetActivitiesService, GetActivityService
from app.services.delete_ativity_service import DeleteActivityService
from app.services.create_activity_service import CreateActivityService

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
    new = CreateActivityService(activity=activity).perform()
    return ActivityWithMessage(activity=new, message='successfully created')


@app.delete('/attributes/{id}')
def delete_activity(activity_id: PositiveInt) -> ActivityWithMessage:
    deleted_activity = DeleteActivityService(activity_id=activity_id).perform()
    if not deleted_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return ActivityWithMessage(activity=deleted_activity, message='successfully deleted')
