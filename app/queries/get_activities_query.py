from pypika import Query, Table, Order

from base_query import BaseQuery


class GetActivitiesQuery(BaseQuery):
    TABLE = Table('activities')

    def __init__(self, fields: list[str] = None):
        self.fields = fields

    def _build(self):
        return Query\
            .from_(self.TABLE).select(*self.fields or '*')\
            .orderby(self.TABLE.start_time, Order.desc)
