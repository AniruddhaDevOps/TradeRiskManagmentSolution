import pandas as pd
import numpy as np
import pytest
from traderiskmangment import BlackScholeForwardPrice


@pytest.fixture
def option_trading():
    trade_date = '2022-11-23'
    expiry_date = '2023-05-10'
    stock_price = 19
    strike_price = 17
    risk_free = 0.005
    sigma = 0.3
    return BlackScholeForwardPrice(trade_date, expiry_date, stock_price, strike_price, risk_free, sigma)

def test_at_the_money(option_trading):
    expected_C = 1.39597
    expected_P = 1.35699

    option_trading.stock_price = 17

    assert pytest.approx(option_trading.C(), 0.001) == expected_C
    assert pytest.approx(option_trading.P(), 0.001) == expected_P

def test_in_the_money(option_trading):
    expected_C = 2.69688
    expected_P = 0.65790

    assert pytest.approx(option_trading.C(), 0.001) == expected_C
    assert pytest.approx(option_trading.P(), 0.001) == expected_P

def test_out_the_money(option_trading):
    expected_C = 0.54279
    expected_P = 2.50381

    option_trading.stock_price = 15

    assert pytest.approx(option_trading.C(), 0.001) == expected_C
    assert pytest.approx(option_trading.P(), 0.001) == expected_P

