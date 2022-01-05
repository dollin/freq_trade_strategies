import numpy as np
import pandas as pd
from functools import reduce
from pandas import DataFrame

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter, IntParameter, IStrategy)

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class RsiStrategy(IStrategy):

    buy_adx = DecimalParameter(20, 50, default=30, space="buy")
    buy_adx_enabled = BooleanParameter(default=False, space="buy")

    sell_adx = IntParameter(50, 100, default=53, space='sell')
    sell_adx_enabled = BooleanParameter(default=False, space="sell")

    buy_rsi = IntParameter(10, 35, default=29, space="buy")
    buy_rsi_enabled = BooleanParameter(default=True, space="buy")

    sell_rsi = IntParameter(65, 85, default=72, space="sell")
    sell_rsi_enabled = BooleanParameter(default=True, space="sell")

    minimal_roi = {"0": 0.361, "60": 100.00}
    stoploss = -1.0
    trailing_stop = False
    timeframe = '15m'
    process_only_new_candles = False
    use_sell_signal = True
    sell_profit_only = True

    ignore_roi_if_buy_signal = False
    startup_candle_count: int = 8
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
        conditions = []

        if self.buy_adx_enabled.value:
            conditions.append(qtpylib.crossed_above(dataframe['adx'], self.buy_adx.value))
        if self.buy_rsi_enabled.value:
            conditions.append(qtpylib.crossed_above(dataframe['rsi'], self.buy_rsi.value))

        conditions.append(dataframe['volume'] > 0)

        if conditions:
            dataframe.loc[reduce(lambda x, y: x & y, conditions), 'buy'] = 1

        # print(f"result for {metadata['pair']}")
        # print(dataframe.tail())
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []

        if self.sell_adx_enabled.value:
            conditions.append(qtpylib.crossed_above(dataframe['adx'], self.sell_adx.value))
        if self.sell_rsi_enabled.value:
            conditions.append(qtpylib.crossed_above(dataframe['rsi'], self.sell_rsi.value))

        conditions.append(dataframe['volume'] > 0)

        if conditions:
            dataframe.loc[reduce(lambda x, y: x & y, conditions), 'sell'] = 1

        # print(f"result for {metadata['pair']}")
        # print(dataframe.tail())
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=6)
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=6)

        return dataframe
