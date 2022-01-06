from freqtrade.strategy import IStrategy

from functools import reduce
from pandas import DataFrame


class BaseStrategy(IStrategy):

    minimal_roi = {
        "0": 0.31,
        "69": 0.114,
        "225": 0.049,
        "549": 0.00
    }

    stoploss = -1.0
    trailing_stop = False
    timeframe = '15m'
    process_only_new_candles = False
    use_sell_signal = True
    sell_profit_only = True

    ignore_roi_if_buy_signal = False

    order_types = {
        'buy': 'market',
        'sell': 'market',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    order_time_in_force = {
        'buy': 'gtc',
        'sell': 'gtc'
    }

    @staticmethod
    def add_conditions(dataframe: DataFrame, conditions: list, side: str):
        dataframe.loc[reduce(lambda x, y: x & y, conditions), side] = 1
