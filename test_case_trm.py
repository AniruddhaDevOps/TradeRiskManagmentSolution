import pytest
from traderiskmangment import BlackScholeForwardPrice


@pytest.fixture
def option_trading():
    trade_date = '2022-11-23'
    expiry_date = '2023-05-10'
    spot_price = 19
    strike_price = 17
    risk_free = 0.005
    sigma = 0.3
    return BlackScholeForwardPrice(trade_date, expiry_date, spot_price, strike_price, risk_free, sigma)

def test_at_the_money(option_trading):
    expected_call_options = 1.39597
    expected_put_options = 1.35699

    option_trading.spot_price = 17

    assert pytest.approx(option_trading.call_options(), 0.001) == expected_call_options
    assert pytest.approx(option_trading.put_options(), 0.001) == expected_put_options

def test_in_the_money(option_trading):
    expected_call_options = 2.69688
    expected_put_options = 0.65790

    assert pytest.approx(option_trading.call_options(), 0.001) == expected_call_options
    assert pytest.approx(option_trading.put_options(), 0.001) == expected_put_options

def test_out_the_money(option_trading):
    expected_call_options = 0.54279
    expected_put_options = 2.50381

    option_trading.spot_price = 15

    assert pytest.approx(option_trading.call_options(), 0.001) == expected_call_options
    assert pytest.approx(option_trading.put_options(), 0.001) == expected_put_options

