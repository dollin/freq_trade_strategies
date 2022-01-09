import sys

from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from base_strategy import BaseStrategy
from pandas import DataFrame

import talib.abstract as ta
from technical.util import resample_to_interval, resampled_merge
import freqtrade.vendor.qtpylib.indicators as qtpylib


class MultipleRsiStrategy(BaseStrategy):

    def resample_timeframe(self, x: int):
        return int(self.timeframe[:-1]) * x

    def resample_key(self, x: int):
        return 'resample_{}_rsi'.format(self.resample_timeframe(x))

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = [dataframe['sma5'] >= dataframe['sma200'],
                      dataframe['rsi'] < dataframe[self.resample_key(8)] - 20
                      ]

        self.add_conditions(dataframe, conditions, 'buy')
        self.log_trends(dataframe, metadata, 'buy')
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = [dataframe['rsi'] > dataframe[self.resample_key(2)],
                      dataframe['rsi'] > dataframe[self.resample_key(8)]
                      ]

        self.add_conditions(dataframe, conditions, 'sell')
        self.log_trends(dataframe, metadata, 'sell')
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
