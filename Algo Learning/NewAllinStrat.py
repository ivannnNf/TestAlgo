import decimal
import backtrader as bt
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

cerebro = bt.Cerebro()

data = bt.feeds.YahooFinanceData(dataname='INDEX_ETHUSD, 1D.csv',
reverse=False,
adjclose=False,
decimals=4,
todate=datetime.datetime(2025, 2, 9))
cerebro.adddata(data)


class AlgoLearningStrategy(bt.Strategy):
   

   params = (
        ('rsi_period', 14),
        ('ema_period', 20),
    )
    
   def __init__(self):
        self.rsi = bt.indicators.RSI(period=self.params.rsi_period)
        self.ema = bt.indicators.EMA(period=self.params.ema_period)
    
   def next(self):
        dt = self.datas[0].datetime.datetime(0)  # Get the current datetime
        close_price = self.datas[0].close[0]  # Get the current close price
        ShortOrLong = ""

        if self.position.size > 0:
            ShortOrLong = "Long Position Open"
        elif self.position.size < 0:
            ShortOrLong = "Short Position Open"
        elif self.position.size == 0:
            ShortOrLong = "No Trades Open"

        print(f"{dt} - Close Price: {close_price} - {ShortOrLong} - {self.position.size}")  # Print datetime & close price

        if self.data.close[0] > self.ema[0] and self.rsi[0] > 60 and self.position.size <= 0:
            self.close()  # Close any existing short positions
            self.buy(size=100)  # Enter a long position

        elif self.data.close[0] < self.ema[0] and self.rsi[0] < 40 and self.position.size >= 0:
            self.close()  # Close any existing long positions
            self.sell(size=100)  # Enter a short position

        else:
            # Optional: Define an exit strategy if needed
            pass

# Backtest setup

cerebro.addstrategy(AlgoLearningStrategy)



cerebro.run()
cerebro.plot(style='candlestick', volume=True, barup='grey', bardown='black')
