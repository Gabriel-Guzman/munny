# --- Do not remove these libs ---
from freqtrade.strategy import IStrategy
from freqtrade.strategy import CategoricalParameter, DecimalParameter, IntParameter
from pandas import DataFrame
# --------------------------------

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

# ShortTradeDurHyperOptLoss, OnlyProfitHyperOptLoss,
#                         SharpeHyperOptLoss, SharpeHyperOptLossDaily,
#                         SortinoHyperOptLoss, SortinoHyperOptLossDaily,
#                         CalmarHyperOptLoss, MaxDrawDownHyperOptLoss,
#                         MaxDrawDownRelativeHyperOptLoss,
#                         ProfitDrawDownHyperOptLoss

class ATRStrategy(IStrategy):
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi"

    # Optimal stoploss designed for the strategy
    # This attribute will be overridden if the config file contains "stoploss"
    stoploss = -0.3

    # Optimal timeframe for the strategy
    timeframe = '5m'

    # begin atr trailing
    buy_atr_period = IntParameter(low=1, high=150, default=5, space='buy', optimize=True)
    buy_hhv = IntParameter(low=2, high=150, default=10, space='buy', optimize=True)
    buy_mult = DecimalParameter(low=0.1, high=10, default=2.5, space='buy', optimize=True)

    sell_atr_period = IntParameter(low=1, high=150, default=5, space='sell', optimize=True)
    sell_hhv = IntParameter(low=2, high=150, default=10, space='sell', optimize=True)
    sell_mult = DecimalParameter(low=0.1, high=10, default=2.5, space='sell', optimize=True)

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
                (self.buy_hhv.value.item())
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
                (self.sell_hhv.value.item())
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
