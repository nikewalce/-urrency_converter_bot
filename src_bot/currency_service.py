class CurrencyService:
    RATES = {
        "USD_RUB": 78.65,
        "RUB_USD": 1 / 78.65,
        "THB_RUB": 2.51,
        "RUB_THB": 1 / 2.51,
        "USD_THB": 31.39,
        "THB_USD": 1 / 31.39
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
    