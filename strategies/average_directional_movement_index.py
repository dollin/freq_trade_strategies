import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from template_strategy import BaseStrategy
from freqtrade.strategy import IntParameter
from pandas import DataFrame

import talib.abstract as ta

'''
    Average Directional Movement Index (ADX).
     - ADX can be used to measure the strength and ability of a trend
     - The ADX indicator is determined as an average of expanding price range values
    
    Plus Directional Indicator (+DI)
     - Is the difference between current highs and previous highs
     - When the +DI moves upwards then there will be an uptrend in the market
     - When the +DI moves downwards then there will be a downtrend in the market
    
    Negative Directional Index (-DI)
     - Is the difference between current lows and previous lows
     - When the -DI moves upwards then there will be a downtrend in the market
     - When the -DI moves downwards then there will be an uptrend in the market
    
    The ADX indicator has a range of 0-100 where 0 denotes the weakest trend and 100 the strongest 
    There are two types of ADX crossovers, positive and negative: -
    
     - Positive Crossover: When the ADX line is above 25 and the +DI line moves from below to above the -DI line
     - Then this indicator is recognized as a bullish ADX crossover or buy signal
     
     - Negative Crossover: When the ADX line is above 25 and the +DI line moves from above to below the -DI line
     - Then it is known as a bearish ADX crossover or sell signal.
'''


class AverageDirectionalMovementIndex(BaseStrategy):

    minimal_roi = {
        "0": 0.376,
        "75": 0.128,
        "134": 0.088,
        "382": 0.056
    }

    startup_candle_count: int = 14

    buy_adx = IntParameter(15, 35, default=32, space="buy")
    buy_adx_shift = IntParameter(15, 35, default=27, space="buy")

    sell_adx = IntParameter(15, 35, default=28, space="sell")

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        buy_conditions = [dataframe['adx'] >= self.buy_adx.value,
                          dataframe['adx'].shift(1) >= self.buy_adx_shift.value,
                          dataframe['plus_di'] >= dataframe['minus_di'],
                          dataframe['plus_di'].shift(1) >= dataframe['minus_di'].shift(1)
                          ]

        self.add_conditions(dataframe, buy_conditions, 'buy')
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        sell_conditions = [dataframe['adx'] >= self.sell_adx.value,
                           dataframe['plus_di'] < dataframe['minus_di']
                           ]

        self.add_conditions(dataframe, sell_conditions, 'sell')
        return dataframe
