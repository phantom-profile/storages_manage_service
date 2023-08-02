from lib.clients.currencies_client import CurrenciesApiClient


class ConvertorError(Exception):
    ...


class CurrencyConverter:
    ALLOWED = CurrenciesApiClient.DEFAULT
    CHOICES = tuple((value, value) for value in ALLOWED)

    def __init__(self, convert_from: str, convert_to: str, amount: float):
        if amount <= 0:
            raise ConvertorError('Converted value must be greater than 0')
        if convert_from not in self.ALLOWED or convert_to not in self.ALLOWED:
            raise ConvertorError('Currency not registered')

        self.convert_from = convert_from
        self.convert_to = convert_to
        self.amount = amount
        self.client = CurrenciesApiClient(self.convert_from, self.convert_to)

    def convert(self) -> dict:
        response = self.client.get_currency()
        if not response['is_successful']:
            raise ConvertorError('Could not fetch current currencies convertion. Try later')
        return {
            "from": self.convert_from,
            "to": self.convert_to,
            "from_value": self.amount,
            "to_value": round(self.get_currency_value(response) * self.amount, 2),
        }

    def get_currency_value(self, response):
        value = response
        for key in ('response_body', 'data', self.convert_to, 'value'):
            if key in value:
                value = value.get(key, {})
        return value or 0
