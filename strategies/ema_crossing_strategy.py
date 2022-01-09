import sys

from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from base_strategy import BaseStrategy
from pandas import DataFrame

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class EmaCrossingStrategy(BaseStrategy):

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[(qtpylib.crossed_above(dataframe['ema5'], dataframe['ema10'])), 'buy'] = 1
        self.log_trends(dataframe, metadata, 'buy')
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[(qtpylib.crossed_above(dataframe['ema10'], dataframe['ema5'])), 'sell'] = 1
        self.log_trends(dataframe, metadata, 'sell')
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)
        dataframe['ema10'] = ta.EMA(dataframe, timeperiod=10)
        return dataframe
