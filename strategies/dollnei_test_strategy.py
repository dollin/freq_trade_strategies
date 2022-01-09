import sys

from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from base_strategy import BaseStrategy

from pandas import DataFrame

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class DollneiTestStrategy(BaseStrategy):

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = [qtpylib.crossed_above(dataframe['ema5'], dataframe['ema10'])]

        self.add_conditions(dataframe, conditions, 'buy')
        self.log_trends(dataframe, metadata, 'buy')

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = [qtpylib.crossed_above(dataframe['ema10'], dataframe['ema5'])]

        self.add_conditions(dataframe, conditions, 'sell')
        self.log_trends(dataframe, metadata, 'sell')
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)
        dataframe['ema10'] = ta.EMA(dataframe, timeperiod=10)
        dataframe['ema20'] = ta.EMA(dataframe, timeperiod=20)

        return dataframe

