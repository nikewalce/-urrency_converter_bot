class CurrencyService:
    RATES = {
        "USD_RUB": 80.33,
        "RUB_USD": 1 / 80.33,
        "THB_RUB": 2.45,
        "RUB_THB": 1 / 2.45,
        "USD_THB": 32.48,
        "THB_USD": 1 / 32.48
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
    