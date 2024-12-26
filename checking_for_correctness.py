import requests
import json
from argument import currency # импорт. список валют



class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(base, quote, amount):

        if base.strip()==quote.strip(): # проверяем не одна ли таже валюта
            raise ConvertionException(f'Невозможно перевести одну и ту же валюту: {base}')

        try:# проверяем если такая валюта
            _base = currency[base.strip()]
        except KeyError:
            raise ConvertionException(f'Не удалось найти валюту {base}')

        try: # проверяем если такая валюта
            _quote = currency[quote.strip()]
        except KeyError:
            raise ConvertionException(f'Не удалось найти валюту {quote}')

        try: # проверяем правильно ли вели количество, необходимой валюты.
            _amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось найти количество {amount}')

        get_result = requests.get(f'''https://min-api.cryptocompare.com/data/price?fsym={_base}&tsyms={_quote}''')

        result = json.loads(get_result.content)[_quote]

        return result