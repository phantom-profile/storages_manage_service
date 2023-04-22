from app.models.activity import BaseActivity, ActivityWithMessage
from app.queries.create_activity_query import CreateActivityQuery


class CreateActivityService:
    def __init__(self, activity: BaseActivity):
        self.activity = activity

    def perform(self) -> ActivityWithMessage:
        creating = CreateActivityQuery(self.activity.dict())
        creating.execute()
        if not creating.is_successful:
            return ActivityWithMessage(activity=self.activity, message=creating.error_message)

        return ActivityWithMessage(activity=self.activity)
