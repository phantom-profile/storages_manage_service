from requests import get, post
from datetime import datetime

from lib.clients.base_client import BaseClient
from storages_manage_service.settings import env_variables


class PayServiceClient(BaseClient):
    TOKEN = env_variables.get('PAYMENT_TOKEN')
    URL = env_variables.get('PAYMENT_URL')

    def get_cards(self):
        self._response = get(
            url=self._build_url("cards"),
            params={'token': self.TOKEN}
        )

        return self._service_response

    def trust_card(self, card_number: str, cvv: str, owner: str,
                   vendor: str, bank: str):
        self._response = post(
            url=self._build_url("cards/trust"),
            params={'token': self.TOKEN},
            json={
                "card_number": card_number,
                "cvv": cvv,
                "owner": owner,
                "payment_system": vendor,
                "bank_name": bank
            }
        )
        return self._service_response
