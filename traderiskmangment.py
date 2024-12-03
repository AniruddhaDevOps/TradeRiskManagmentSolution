import pandas as pd
import numpy as np
from scipy.stats import norm
from datetime import datetime


class BlackScholeForwardPrice:

    def __init__(self, trade_date: str, expiry_date: str, stock_price: float, strike_price: float, risk_free: float, sigma: float):
        """
        Initialize the BlackScholeForwardPrice model with provide data trade and expiry dates, 
        current stock price, strike price, risk-free rate, and volatility.

        Parameters:
        trade_date (str): The date when the option is traded (YYYY-MM-DD).
        expiry_date (str): The expiry date of the option (YYYY-MM-DD).
        stock_price (float): Current stock price.
        strike_price (float): Strike price of the option.
        risk_free(float): Risk-free interest rate (as a decimal).
        sigma (float): Volatility of the stock (as a decimal).
        """
        self.trade_date = self._validate_date(trade_date, "trade_date")
        self.expiry_date = self._validate_date(expiry_date, "expiry_date")
        self.stock_price = self._validate_float(stock_price, "Spot price (S)")
        self.strike_price = self._validate_float(strike_price, "Exercise price (K)")
        self.risk_free = self._validate_float(risk_free, "Risk free rate (r)")
        self.sigma = self._validate_float(sigma, "sigma")

    def _validate_date(self, value, name):
        if not isinstance(value, str):
            raise ValueError(f"{name} should be a string")
        try:
            return datetime.strptime(value, "%Y-%m-%d")
        except:
            raise ValueError(f"{name} should be correctly formatted: '%Y-%m-%d' (e.g '2024-10-15')")

    def _validate_float(self, value, name):
        if not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be an integer or float")
        return value

    def T(self):
        """Calculate the time to expiry"""
        return (self.expiry_date - self.trade_date).days / 365

    def F(self):
        """Calculate the forward price."""
        return self.stock_price * np.exp(self.risk_free * self.T())

    def d1(self):
        """Calculate d1 used in the Black-Scholes formula."""
        return (np.log(self.F() / self.strike_price) + (self.sigma ** 2 / 2) * self.T()) / (self.sigma * np.sqrt(self.T()))

    def d2(self):
        """Calculate d2 used in the Black-Scholes formula."""
        return self.d1() - self.sigma * np.sqrt(self.T())

    def C(self):
        """Calculate the call option price."""
        return np.exp(-self.risk_free * self.T()) * (self.F() * norm.cdf(self.d1()) - self.strike_price * norm.cdf(self.d2()))

    def P(self):
        """Calculate the put option price."""
        return self.C() - self.stock_price + self.strike_price * np.exp(-self.risk_free * self.T())

    def __str__(self) -> str:
        return (f'Option Trading : \n trade_date: {self.trade_date} \n expiry_date: {self.expiry_date}\n spot_price: {self.stock_price}\nd1: {self.d1()} '
                f'\nd2: {self.d2()} \n strike_price : {self.strike_price} \n call_price : {self.C()} \n put_price (P): {self.P()}')
    

class VaRCalculation:

    def __init__(self, market_rate_1: np.array, market_rate_2: np.array, spot_price_1: float, spot_price_2: float):
        """
        Initialize the Value-at-Risk model with market rates and spot prices of two currencies.

        Parameters:
        market_rate_1 (np.array): The market rates per day of currency 1.
        market_rate_2 (np.array): The market rates per day of currency 2.
        spot_price_1: Spot price of holdings in currency 1.
        spot_price_2: Spot price of holdings in currency 2. 
        """

        self.market_rate_1 = self._validate_array(market_rate_1, "market_rate_1")
        self.market_rate_2 = self._validate_array(market_rate_2, "market_rate_2")
        self.spot_price_1 = self._validate_float(spot_price_1, "Total value of holdings in currency 1 (spot_price_1)")
        self.spot_price_2 = self._validate_float(spot_price_2, "Total value of holdings in currency 2 (spot_price_2)")

    def _validate_array(self, value, name):
        if not isinstance(value, np.ndarray):
            raise ValueError(f"The market rates of currency ({name}) should be a numpy array.")
        return value

    def _validate_float(self, value, name):
        if not isinstance(value, (int, float)):
            raise ValueError(f"{name} should be integer or float")
        return value

    def pnl_vector(self, spot_price, market_rate) -> np.array:
        return (np.exp(np.log(market_rate[:-1] / market_rate[1:])) - 1) * spot_price
    
    def total_pnl(self) -> np.array:
        return np.sort(self.pnl_vector(self.spot_price_1, self.market_rate_1) + self.pnl_vector(self.spot_price_2, self.market_rate_2))

    def var_1d(self) -> float:
        return (0.4 * self.total_pnl()[1]) + (0.6 * self.total_pnl()[2])
    
    def __str__(self) -> str:
        return (f' spot_price_1: {self.spot_price_1}\n spot_price_2: {self.spot_price_2} \n VaR-One Day: {self.var_1d()}\n')


def import_excel_data() -> np.array:
    df = pd.read_excel('/Users/aniruddhamacuser/Aniruddha/Project/LearningCode/excel/varcalulationdata.xlsx')
    ccy1 = np.array(df['market_rate_ccy1'].to_list())
    ccy2 = np.array(df['market_rate_ccy2'].to_list())
    return ccy1, ccy2


ccy1, ccy2 = import_excel_data()
option = BlackScholeForwardPrice('2022-11-23', '2023-05-10', 19, 17, 0.005, 0.3)
var = VaRCalculation(ccy1, ccy2, 153084.81, 95891.51)
print("BlackScholeForwardPrice Calculation:\n" + str(option))
print("VaR Calculation for One Day:\n" + str(var))
