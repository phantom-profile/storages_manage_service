from app.queries.get_activities_query import GetActivitiesQuery
from app.models.activity import Activity, ActivitiesFilter


class GetActivitiesService:
    def __init__(self, params=None):
        self.activities = []
        if not params:
            self.params = {}
        else:
            self.params = params.dict()
        self.query = GetActivitiesQuery(filters=self.params)

    def perform(self) -> list[Activity]:
        self.query.execute()
        if not self.query.is_successful or not self.query.result:
            return self.activities

        for row in self.query.result:
            self.activities.append(Activity(**row))

        return self.activities


class GetActivityService:
    def __init__(self, activity_id: int):
        self.activity_id = activity_id

    def perform(self) -> Activity | None:
        query = ActivitiesFilter(id=self.activity_id, per_page=1)
        result = GetActivitiesService(query).perform()
        if not result:
            return None

        return result[0]
