import pytest
from src_bot.currency_service import CurrencyService

@pytest.mark.parametrize("rates_key, amount", [
    ("USD_RUB", 80.33),
    ("RUB_USD", 1 / 80.33),
    ("THB_RUB", 2.45),
    ("RUB_THB", 1 / 2.45),
    ("USD_THB", 32.48),
    ("THB_USD", 1 / 32.48),
])
def test_get_rate(rates_key, amount):
    service = CurrencyService()
    assert service.get_rate(rates_key) == amount

def test_get_rate_unknown_pair():
    assert CurrencyService.get_rate("EUR_USD") is None

@pytest.mark.parametrize("pair,amount", [
    ("USD_RUB", 100),
    ("RUB_USD", 100),
    ("THB_RUB", 100),
    ("RUB_THB", 100),
    ("USD_THB", 100),
    ("THB_USD", 100),
])
def test_convert_valid_pairs(pair, amount):
    result = CurrencyService.convert(amount, pair)
    expected = amount * CurrencyService.get_rate(pair)
    assert result == expected

def test_convert_unknown_pair_raises():
    with pytest.raises(ValueError, match="Unknown currency pair"):
        CurrencyService.convert(100, "EUR_USD")

#Чувствительность к регистру
def test_get_rate_case_sensitivity():
    assert CurrencyService.get_rate("usd_rub") is None

#Граничные значения
def test_convert_zero_amount():
    result = CurrencyService.convert(0, "USD_RUB")
    assert result == 0

def test_convert_negative_amount():
    result = CurrencyService.convert(-50, "USD_RUB")
    assert result == -50 * 80.33
