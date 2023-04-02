from pypika import Query, Table, Order


class GetActivitiesQuery:
    TABLE = Table('activities')

    def __init__(self, fields: list[str] = None):
        self.fields = fields

    def build(self, sql=True):
        query = Query\
            .from_(self.TABLE).select(*self.fields or '*')\
            .orderby(self.TABLE.start_time, Order.desc)

        return query if not sql else query.get_sql()
