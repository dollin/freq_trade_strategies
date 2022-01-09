import datetime
import logging
import pandas
from freqtrade.strategy import IStrategy

from functools import reduce
from pandas import DataFrame
from datetime import datetime

log = logging.getLogger(__name__)


class BaseStrategy(IStrategy):

    minimal_roi = {
        "0": 0.31,
        "69": 0.114,
        "225": 0.068,
        "549": 0.0
    }

    stoploss = -1.0
    trailing_stop = False
    timeframe = '15m'
    process_only_new_candles = False
    use_sell_signal = True
    sell_profit_only = True

    ignore_roi_if_buy_signal = False

    order_types = {
        'buy': 'limit',
        'sell': 'limit',
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

    @staticmethod
    def log_trends(dataframe: DataFrame, metadata: dict, side: str):
        intervals = [5, 20, 35, 50]
        if side == 'sell':
            intervals = [x + 2 for x in intervals]

        # log all buy trends every 15 minutes
        if datetime.now().minute in intervals and datetime.now().second < 10:
            pandas.set_option('display.max_columns', None)
            log.info(f"Buy trend for pair: [{metadata.get('pair')}]")
            log.info(f"Buy dataframe:\n[\n{dataframe.tail(2)}\n]")
