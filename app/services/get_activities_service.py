from app.queries.get_activities_query import GetActivitiesQuery
from app.models.activity import Activity


class GetActivitiesService:
    def __init__(self, params=None):
        self.activities = []
        self.params = params
        self.query = GetActivitiesQuery()

    def perform(self) -> list[Activity]:
        self.query.execute()
        if not self.query.is_successful or not self.query.result:
            return self.activities

        for row in self.query.result:
            self.activities.append(Activity(**row))

        return self.activities
