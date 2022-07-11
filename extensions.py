import requests
import json
from config import VALUTA


class Converter:
    @staticmethod
    def get_price(quote, base, amount):
        if quote == base:
            raise ConversionException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            VALUTA[quote]
        except KeyError:
            raise ConversionException(f'Не удлалось обработать валюту {quote}')

        try:
            VALUTA[base]
        except KeyError:
            raise ConversionException(f'Не удлалось обработать валюту {base}')

        try:
            amount = int(amount)
        except ValueError:
            raise ConversionException('Введено некорректное число')

        data = json.loads(requests.get(
            'https://cdn.cur.su/api/cbr.json').content)
        result = data['rates'][VALUTA[base]] / data['rates'][VALUTA[quote]]
        result *= amount
        return result


class ConversionException(Exception):
    pass
