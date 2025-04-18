import requests

URL_API_USD_RATE = 'https://api.exchangerate-api.com/v4/latest/USD'

class CurrencyManager:
    def __init__(self, auto_fetch: bool = True):
        self.rates = {}
        if auto_fetch:
            self.fetch_rates()

    def fetch_rates(self):
        try:
            response = requests.get(URL_API_USD_RATE, timeout=5)
            if response.status_code != 200:
                raise Exception(f"Exchange API error: {response.status_code}")
            data = response.json()
            self.rates = data["rates"]
        except Exception as e:
            print(f"Error fetching exchange rates: {e}")
            self.rates = {}

    def get_rate_between(self, from_currency: str, to_currency: str) -> float:
        """ מחזיר את יחס ההמרה בין שני מטבעות (כולל USD או בלי) """
        if from_currency == to_currency:
            return 1.0

        from_rate = self.rates.get(from_currency)
        to_rate = self.rates.get(to_currency)

        if not from_rate or not to_rate:
            raise ValueError(f"Invalid currency conversion: {from_currency} to {to_currency}")

        return to_rate / from_rate

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """ ממיר סכום בין שני מטבעות כלשהם """
        rate = self.get_rate_between(from_currency, to_currency)
        return round(amount * rate, 2)



