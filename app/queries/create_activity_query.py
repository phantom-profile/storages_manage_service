from pypika import Query, Table

from app.queries.base_query import BaseQuery


class CreateActivityQuery(BaseQuery):
    TABLE = Table('activities')

    def __init__(self, params: dict):
        super().__init__()
        self.params = params

    def _build(self):
        return Query\
            .into(self.TABLE).columns(*self.params.keys())\
            .insert(*self.params.values())
