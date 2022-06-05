# --- Do not remove these libs ---
from freqtrade.strategy import IStrategy
from freqtrade.strategy import CategoricalParameter, DecimalParameter, IntParameter
from pandas import DataFrame
# --------------------------------

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import os
import json

# ShortTradeDurHyperOptLoss, OnlyProfitHyperOptLoss,
#                         SharpeHyperOptLoss, SharpeHyperOptLossDaily,
#                         SortinoHyperOptLoss, SortinoHyperOptLossDaily,
#                         CalmarHyperOptLoss, MaxDrawDownHyperOptLoss,
#                         MaxDrawDownRelativeHyperOptLoss,
#                         ProfitDrawDownHyperOptLoss
try:
    if os.path.exists('user_data/strategies/ATRStrategyHO.json'):
        f = open('user_data/strategies/ATRStrategyHO.json')
        data = json.load(f)
    else:
        data = None
except:
    print("error opening file")
    data = None

class ATRStrategyHO(IStrategy):
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi"

    # Optimal stoploss designed for the strategy
    # This attribute will be overridden if the config file contains "stoploss"
    stoploss = -0.3

    # Optimal timeframe for the strategy
    timeframe = '5m'

    minimal_roi = {
        "60": 0.01,
        "30": 0.03,
        "20": 0.04,
        "0": 0.05
    }

    # begin atr trailing
    buy_atr_period = IntParameter(low=1, high=150, default=5, space='buy', optimize=True)
    buy_hhv = IntParameter(low=2, high=150, default=10, space='buy', optimize=True)
    buy_mult = DecimalParameter(low=0.1, high=10, default=2.5, space='buy', optimize=True)

    sell_atr_period = IntParameter(low=1, high=150, default=5, space='sell', optimize=True)
    sell_hhv = IntParameter(low=2, high=150, default=10, space='sell', optimize=True)
    sell_mult = DecimalParameter(low=0.1, high=10, default=2.5, space='sell', optimize=True)

    # Buy hyperspace params:
    buy_params = {
        "buy_atr_period": data['params']['buy']['buy_atr_period'] if data is not None else 62,
        "buy_hhv": data['params']['buy']['buy_hhv'] if data is not None else 146,
        "buy_mult": data['params']['buy']['buy_mult'] if data is not None else 0.396,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_atr_period": data['params']['sell']['sell_atr_period'] if data is not None else 121,
        "sell_hhv": data['params']['sell']['sell_hhv'] if data is not None else 142,
        "sell_mult": data['params']['sell']['sell_mult'] if data is not None else 8.605,
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # begin my indicators

        dataframe['atr'] = ta.ATR(dataframe, self.buy_atr_period.value)
        dataframe['sell_atr'] = ta.ATR(dataframe, self.sell_atr_period.value)
        # dataframe['atr'] = ta.ATR(dataframe, 448)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the buy signal for the given dataframe
        :param dataframe: DataFrame
        :return: DataFrame with buy column
        """

        try:
            prev = ta.MAX(
                dataframe['high'].sub(self.buy_mult.value * dataframe['atr']).squeeze(),
                (self.buy_hhv.value.item() if hasattr(self.buy_hhv.value, 'item') else self.buy_hhv.value)
                # dataframe['high'].sub(0.156 * dataframe['atr']).squeeze(),
                # 154
            )
        except:
            print("buy error happened",
                  type(dataframe['high'].sub(self.buy_mult.value * dataframe['atr'], fill_value=0).squeeze()),
                  self.buy_hhv.value, type(self.buy_hhv.value), self.buy_hhv.value.item(), dataframe['high'], dataframe['atr'])
            exit(1)

        ts = ''
        if dataframe.shape[0] < 16:
            ts = dataframe['close']
        else:
            ts = prev

        dataframe.loc[
            (
                    (dataframe['volume'] > 0) &
                    qtpylib.crossed_above(dataframe['close'], prev)
            ),
            'buy'
        ] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the sell signal for the given dataframe
        :param dataframe: DataFrame
        :return: DataFrame with buy column
        """
        try:
            prev = ta.MAX(
                dataframe['high'].sub(self.sell_mult.value * dataframe['sell_atr'], fill_value=0).squeeze(),
                (self.sell_hhv.value.item() if hasattr(self.sell_hhv.value, 'item') else self.sell_hhv.value)
                # dataframe['high'].sub(8.27 * dataframe['atr'], fill_value=0).squeeze(),
                # 51
            )
        except:
            print("sell error happened", self.sell_hhv.value, type(self.sell_hhv.value), dataframe['high'], dataframe['atr'], type(dataframe['high'].sub(self.sell_mult.value * dataframe['atr'], fill_value=0).squeeze()))
            exit(1)

        ts = ''
        if dataframe.shape[0] < 16:
            ts = dataframe['close']
        else:
            ts = prev

        dataframe.loc[
            (
                    qtpylib.crossed_below(dataframe['close'], prev)
            ),
            'sell'
        ] = 1

        return dataframe
