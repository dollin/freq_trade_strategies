import numpy as np
import pandas as pd
from pandas import DataFrame

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter, IStrategy, IntParameter)

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class DollneiTestStrategy(IStrategy):
    minimal_roi = {"0": 100.00}
    stoploss = -1.25
    trailing_stop = False
    timeframe = '15m'
    process_only_new_candles = False
    use_sell_signal = True
    sell_profit_only = True
    ignore_roi_if_buy_signal = False
    startup_candle_count: int = 0

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

    def informative_pairs(self):
        return []

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                qtpylib.crossed_above(dataframe['ema5'], dataframe['ema10'])
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                qtpylib.crossed_above(dataframe['ema10'], dataframe['ema5'])
            ),
            'sell'] = 1
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)
        dataframe['ema10'] = ta.EMA(dataframe, timeperiod=10)
        dataframe['ema20'] = ta.EMA(dataframe, timeperiod=20)

        return dataframe

