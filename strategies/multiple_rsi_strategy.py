import numpy as np
import pandas as pd
from functools import reduce
from pandas import DataFrame

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter, IStrategy, IntParameter)

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame

import talib.abstract as ta
from technical.util import resample_to_interval, resampled_merge


class MultipleRsiStrategy(IStrategy):
    minimal_roi = {"0": 0.284, "60": 100.00}
    use_sell_signal = True
    sell_profit_only = True
    ignore_roi_if_buy_signal = False
    stoploss = -1.25
    timeframe = '15m'
    trailing_stop = False
    process_only_new_candles = False
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

    def resample_timeframe(self, x: int):
        return int(self.timeframe[:-1]) * x

    def resample_key(self, x: int):
        return 'resample_{}_rsi'.format(self.resample_timeframe(x))

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []

        conditions.append(dataframe['sma5'] >= dataframe['sma200'])
        conditions.append(dataframe['rsi'] < dataframe[self.resample_key(8)] - 20)

        dataframe.loc[reduce(lambda x, y: x & y, conditions), 'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []

        conditions.append(dataframe['rsi'] > dataframe[self.resample_key(2)])
        conditions.append(dataframe['rsi'] > dataframe[self.resample_key(8)])

        dataframe.loc[reduce(lambda x, y: x & y, conditions), 'sell'] = 1
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe['sma5'] = ta.SMA(dataframe, timeperiod=5)
        dataframe['sma200'] = ta.SMA(dataframe, timeperiod=200)

        dataframe2 = resample_to_interval(dataframe, self.resample_timeframe(2))
        dataframe8 = resample_to_interval(dataframe, self.resample_timeframe(8))

        # compute our RSI's
        dataframe2['rsi'] = ta.RSI(dataframe2, timeperiod=6)
        dataframe8['rsi'] = ta.RSI(dataframe8, timeperiod=6)

        # merge dataframe back together
        dataframe = resampled_merge(dataframe, dataframe2)
        dataframe = resampled_merge(dataframe, dataframe8)

        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=6)
        dataframe.fillna(method='ffill', inplace=True)

        return dataframe
