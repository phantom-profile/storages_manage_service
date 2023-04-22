from app.models.activity import BaseActivity, Activity
from app.queries.create_activity_query import CreateActivityQuery
from app.services.get_activities_service import GetActivityService


class CreateActivityService:
    def __init__(self, activity: BaseActivity):
        self.activity = activity

    def perform(self) -> BaseActivity | None:
        creating = CreateActivityQuery(self.activity.dict())
        creating.execute()
        if not creating.is_successful:
            return None

        return self.activity
