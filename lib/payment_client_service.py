# c9af947d-af8f-473d-beda-d04e05719203

from requests import get

a = get("http://127.0.0.1:8002/cards", params={"token": "c9af947d-af9f-473d-beda-d04e05719203"})
print(a.status_code)