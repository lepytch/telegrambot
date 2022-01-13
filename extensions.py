import json
import requests
from config import exchanges, headers


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, rate, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            rate_key = exchanges[rate.lower()]
        except KeyError:
            raise APIException(f"Валюта {rate} не найдена!")

        if base_key == rate_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')
        r = requests.get(f"https://currency-converter5.p.rapidapi.com/"
                         f"currency/convert", headers=headers,
                         params={"from": {base_key}, "to": {rate_key}, "amount": {amount}})
        resp = json.loads(r.content)
        calculation = resp['rates'][rate_key]['rate_for_amount']
        message = f"Цена {amount} {base} в {rate} : {calculation}"
        return message
