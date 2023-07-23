class GetParamsFilter:
    __slots__ = ('params', 'is_valid')

    ORDER_FIELDS = ('name', 'location', 'id', 'trucks_count',)
    ORDERS_MAP = {
        'asc': '',
        'desc': '-'
    }

    DEFAULT_FIELD = 'id'
    DEFAULT_ORDER = 'desc'

    def __init__(self, params: dict):
        self.params = params
        self.is_valid = False

        self.__add_defaults()
        self.__validate()
        self.__clean()

    @property
    def sort_string(self) -> str:
        order = self.params['order']
        return f"{self.ORDERS_MAP[order]}{self.params['sort']}"

    def __clean(self):
        if self.params['order'] == 'desc':
            change_to = 'asc'
        else:
            change_to = 'desc'
        self.params = self.params | {'change_to': change_to}

    def __validate(self):
        correct_order = self.params['order'] in self.ORDERS_MAP.keys()
        correct_sort = self.params['sort'] in self.ORDER_FIELDS
        self.is_valid = correct_sort and correct_order

    def __add_defaults(self):
        self.params = self.params | {
            'order': self.params.get('order', self.DEFAULT_ORDER),
            'sort': self.params.get('sort', self.DEFAULT_FIELD)
        }
