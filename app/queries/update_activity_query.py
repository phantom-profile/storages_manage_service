from pypika import Query, Table

from app.queries.base_query import BaseQuery


class UpdateActivityQuery(BaseQuery):
    TABLE = Table('activities')

    def __init__(self, params: dict):
        super().__init__()
        self.params = params

    def _build(self):
        raw_query = self.TABLE.update().where(self.TABLE.id == self.params['id'])
        for column, value in self.params.items():
            raw_query = raw_query.set(column, value)
        return raw_query
