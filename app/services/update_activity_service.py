from app.models.activity import UpdateActivity, ActivityWithMessage
from app.queries.update_activity_query import UpdateActivityQuery
from app.services.get_activities_service import GetActivityService


class UpdateActivityService:
    def __init__(self, activity_id: int, activity: UpdateActivity):
        self.activity_id = activity_id
        self.activity_attributes = activity

    def perform(self) -> ActivityWithMessage | None:
        activity = GetActivityService(activity_id=self.activity_id).perform()
        if not activity:
            return None

        updating = UpdateActivityQuery(self.activity_attributes.dict(exclude_unset=True) | {'id': self.activity_id})
        updating.execute()
        if not updating.is_successful:
            return ActivityWithMessage(activity=activity, message=updating.error_message)

        return ActivityWithMessage(activity=GetActivityService(activity_id=self.activity_id).perform())
