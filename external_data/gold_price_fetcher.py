import finnhub

class GoldPriceFetcher:
    DEFAULT_API_KEY = 'cvg3hn1r01qgvsqnbbpgcvg3hn1r01qgvsqnbbq0'

    def __init__(self, api_key: str = None):
        self.api_key = api_key or self.DEFAULT_API_KEY
        self.client = finnhub.Client(api_key=self.api_key)

    def get_price_per_gram(self) -> float | None:
        """ מחזיר את מחיר הזהב לגרם בדולרים, או None במקרה של שגיאה """
        try:
            quote = self.client.quote('GLD')
            price = quote['c']  # המחיר הנוכחי של GLD

            if not price or price <= 0:
                raise ValueError("Invalid GLD price from API")

            price_per_ounce = price * 10.77  # יחס המרה מ-GLD לאונקיית זהב
            price_per_gram = price_per_ounce / 31.1035

            return round(price_per_gram, 2)

        except Exception as e:
            print(f"❌ Error fetching gold price: {e}")
            return None

    def calculate_price_for_grams(self, grams: float) -> float | None:
        """ מחשב כמה זה עולה בדולרים עבור X גרם זהב """
        price_per_gram = self.get_price_per_gram()
        if price_per_gram is None:
            return None
        return round(price_per_gram * grams, 2)

    def calculate_grams_for_amount(self, amount: float) -> float | None:
        """ מחשב כמה גרמים אפשר לקנות בסכום כסף נתון בדולרים """
        price_per_gram = self.get_price_per_gram()
        if price_per_gram is None or price_per_gram == 0:
            return None
        return round(amount / price_per_gram, 2)
