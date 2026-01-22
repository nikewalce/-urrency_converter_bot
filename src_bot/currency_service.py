import requests
#https://app.exchangerate-api.com/dashboard
class CurrencyService:
    RATES_API_USD = requests.get("https://v6.exchangerate-api.com/v6/971142aa6db9dab8b7e92852/latest/USD")
    RATES_API_THB = requests.get("https://v6.exchangerate-api.com/v6/971142aa6db9dab8b7e92852/latest/THB")
    RATES = {
        "USD_RUB": RATES_API_USD.json()["conversion_rates"]["RUB"],
        "RUB_USD": 1 / RATES_API_USD.json()["conversion_rates"]["RUB"],
        "THB_RUB": RATES_API_THB.json()["conversion_rates"]["RUB"],
        "RUB_THB": 1 / RATES_API_THB.json()["conversion_rates"]["RUB"],
        "USD_THB": RATES_API_USD.json()["conversion_rates"]["THB"],
        "THB_USD": 1 / RATES_API_USD.json()["conversion_rates"]["THB"]
    }

    @classmethod
    def get_rate(cls, pair: str) -> float:
        return cls.RATES.get(pair)

    @classmethod
    def convert(cls, amount: float, pair: str) -> float:
        rate = cls.get_rate(pair)
        if rate is None:
            raise ValueError("Unknown currency pair")
        return amount * rate
