import sys

from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from base_strategy import BaseStrategy
from pandas import DataFrame
from freqtrade.strategy import IntParameter

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class RsiStrategy(BaseStrategy):

    buy_rsi = IntParameter(10, 35, default=28, space="buy")
    sell_rsi = IntParameter(65, 85, default=72, space="sell")

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = [qtpylib.crossed_above(dataframe['rsi'], self.buy_rsi.value),
                      dataframe['volume'] > 0
                      ]

        self.add_conditions(dataframe, conditions, 'buy')
        self.log_trends(dataframe, metadata, 'buy')
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        conditions = [qtpylib.crossed_above(dataframe['rsi'], self.sell_rsi.value),
                      dataframe['volume'] > 0
                      ]

        self.add_conditions(dataframe, conditions, 'sell')
        self.log_trends(dataframe, metadata, 'sell')

        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=6)

        return dataframe
