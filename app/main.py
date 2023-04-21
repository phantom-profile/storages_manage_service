from fastapi import FastAPI
from app.models.activity import ActivityList

app = FastAPI()


@app.get('/')
def main_page():
    return {'hello': 'world'}


@app.get('/activities')
def activities_list(query: str | None = None) -> ActivityList:
    activities = ActivityList(activities=[], count=0)
    return activities
