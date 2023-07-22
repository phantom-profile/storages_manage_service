class GetParamsFilter:
    __slots__ = ('params',)

    ORDER_FIELDS = ('name', 'location', 'id', 'trucks_count',)
    ORDERS = ('asc', 'desc',)

    DEFAULT_FIELD = 'id'
    DEFAULT_ORDER = 'desc'

    def __init__(self, params: dict):
        self.params = params | {
            'order': params.get('order', self.DEFAULT_ORDER),
            'sort': params.get('sort', self.DEFAULT_FIELD)
        }

    def is_valid(self) -> bool:
        return self.params['order'] in self.ORDERS and self.params['sort'] in self.ORDER_FIELDS

    def sort_string(self) -> str:

    def cleaned(self) -> dict:
        if self.params['order'] == 'desc':
            order = '-'
            change_to = 'asc'
        else:
            order = ''
            change_to = 'desc'
        return self.params | {'order': order, 'change_to': change_to}
