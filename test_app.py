import pytest

from app_functions import build_currency_list, convert


def test_convert_eur_usd():
    rates = {"EUR": 1, "USD": 1.1}
    assert round(convert(10, "EUR", "USD", rates), 2) == 11.0


def test_convert_usd_eur():
    rates = {"EUR": 1, "USD": 1.1}
    assert round(convert(11, "USD", "EUR", rates), 2) == 10.0


def test_convert_amount_zero_raises():
    rates = {"EUR": 1, "USD": 1.1}
    with pytest.raises(ValueError):
        convert(0, "EUR", "USD", rates)


def test_convert_amount_negative_raises():
    rates = {"EUR": 1, "USD": 1.1}
    with pytest.raises(ValueError):
        convert(-5, "EUR", "USD", rates)


def test_convert_same_currency_raises():
    rates = {"EUR": 1, "USD": 1.1}
    with pytest.raises(ValueError):
        convert(10, "EUR", "EUR", rates)


def test_build_currency_list_no_extra():
    rates = {"EUR": 1, "USD": 1.1}
    assert build_currency_list(rates) == ["EUR", "USD"]


def test_build_currency_list_adds_missing_extra():
    rates = {"EUR": 1, "USD": 1.1, "GBP": 0.85}
    result = build_currency_list(rates, extra_currencies=["GBP", "CAD"])
    assert result == ["EUR", "USD", "GBP"]


def test_build_currency_list_ignores_extra_not_in_rates():
    rates = {"EUR": 1, "USD": 1.1}
    result = build_currency_list(rates, extra_currencies=["CAD"])
    assert result == ["EUR", "USD"]


def test_build_currency_list_no_duplicates():
    rates = {"EUR": 1, "USD": 1.1}
    result = build_currency_list(rates, extra_currencies=["USD"])
    assert result == ["EUR", "USD"]
