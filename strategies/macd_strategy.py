import sys

from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from base_strategy import BaseStrategy
from pandas import DataFrame

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class MacdStrategy(BaseStrategy):

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['ao'] = qtpylib.awesome_oscillator(dataframe)

        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = [dataframe['macd'] > 0,
                      dataframe['ao'] > 0,
                      dataframe['ao'].shift()
                      ]

        self.add_conditions(dataframe, conditions, 'buy')
        self.log_trends(dataframe, metadata, 'buy')

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = [dataframe['macd'] < 0,
                      dataframe['ao'] < 0,
                      dataframe['ao'].shift() > 0
                      ]

        self.add_conditions(dataframe, conditions, 'sell')
        self.log_trends(dataframe, metadata, 'sell')

        return dataframe
