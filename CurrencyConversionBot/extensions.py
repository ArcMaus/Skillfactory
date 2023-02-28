import requests
import json
from config import keys, API_KEY


class ConvertionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно конвертировать одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')
        url = f'https://api.apilayer.com/fixer/convert?to={base_ticker}&from={quote_ticker}&amount={amount}'
        payload = {}
        headers = {'apikey': API_KEY}
        response = requests.request('GET', url, headers=headers, data=payload)
        # исходный объект получается словарем, поэтому далее превращаем его в список и получаем значения всех его ключей
        full_result = list(json.loads(response.content).values())
        # нужный нам результат находится в последнем элементе списка, поэтому обращаемся только к нему
        total_base = full_result[-1]
        return total_base

# Пример ответа сервиса fixer без обработки:
# {
#   "date": "2023-02-28",
#   "info": {
#     "rate": 1.05815,
#     "timestamp": 1677615243
#   },
#   "query": {
#     "amount": 1,
#     "from": "EUR",
#     "to": "USD"
#   },
#   "result": 1.05815,
#   "success": true
# }