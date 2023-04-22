from pypika import Query, Table, Order

from app.queries.base_query import BaseQuery


class GetActivitiesQuery(BaseQuery):
    TABLE = Table('activities')
    DEFAULT_ORDER = Order.desc
    DEFAULT_SORT_COLUMS = (TABLE.id,)
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 50

    def __init__(self, fields: list[str] = None, filters=None):
        super().__init__()
        self.fields = fields
        self.filters = filters or {}
        self.raw_query = Query.from_(self.TABLE).select(*self.fields or '*')

    def _build(self):
        self.filter()
        self.order()
        self.paginate()

        return self.raw_query

    def filter(self):
        ids_in = self.filters.get('id')
        title_like = self.filters.get('title_like')
        if ids_in:
            self.raw_query = self.raw_query.where(self.TABLE.id.isin((ids_in,)))
        if title_like:
            self.raw_query = self.raw_query.where(self.TABLE.title.like(f'%{title_like}%'))

    def order(self):
        sort_fields = self.filters.get('sort_by') or self.DEFAULT_SORT_COLUMS
        self.raw_query = self.raw_query.orderby(sort_fields, order=self.sql_order())

    def paginate(self):
        page = self.filters.get('page', self.DEFAULT_PAGE)
        per_page = self.filters.get('per_page', self.DEFAULT_PER_PAGE)
        self.raw_query = self.raw_query.offset((page - 1) * per_page).limit(per_page)

    def sql_order(self):
        return {
            'asc': Order.asc,
            'desc': Order.desc
        }.get(self.filters.get('order')) or self.DEFAULT_ORDER
