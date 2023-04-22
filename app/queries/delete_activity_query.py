from pypika import Query, Table

from app.queries.base_query import BaseQuery


class DeleteActivityQuery(BaseQuery):
    TABLE = Table('activities')

    def __init__(self, activity_id: int):
        super().__init__()
        self.activity_id = activity_id

    def _build(self):
        return Query.from_(self.TABLE).delete()\
            .where(self.TABLE.id == self.activity_id)
