# Create a Strategy

import datetime
import backtrader as bt 
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" Line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None

        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED {}'.format(order.executed.price))
            elif order.issell():
                self.log('SELL EXECUTED {}'.format(order.executed.price))

            self.bar_executed = len(self)

        self.order=None




    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('close, %.4f' % self.dataclose[0])
        if self.order :
            return
        

        if not self.position:

            if self.dataclose[0] < self.dataclose[-1]:
                # current close less than previous close

                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than the previous close


                    # Check if there is enough cash to buy
                    cash = self.broker.get_cash()
                    price = self.dataclose[0]
                    size = 10
                    if cash >= price * size:
                        # BUY, BUY, BUY!!! (with all possible default parameters)
                        self.log('BUY CREATE, %.4f' % self.dataclose[0])
                        self.buy(size=size)
                    else:
                        self.log('Not enough cash to buy')

        else:
            if len(self) >= (self.bar_executed + 5):
                self.log("SELL CREATED {}".format(self.dataclose[0]))
                self.order = self.sell()






class RSIEMAStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),
        ('sma_period', 20),
    )
    
    def __init__(self):
        self.rsi = bt.indicators.RSI(period=self.params.rsi_period)
        self.ema = bt.indicators.SMA(period=self.params.sma_period)
    
    def next(self):
        dt = self.datas[0].datetime.datetime(0)  # Get the current datetime
        close_price = self.datas[0].close[0]  # Get the current close price
        ShortOrLong = ""

        if self.order:
            return  # Avoid multiple orders


        

        if self.data.close[0] > self.ema[0] and self.rsi[0] > 60 and self.position.size <= 0:
            self.order = self.close(exectype=bt.Order.Close) # Close any existing short positions
            self.order = self.buy(size=10, exectype=bt.Order.Close)
            print(f"Buy Price: {self.data.close[0]} - {dt}")

        elif self.data.close[0] < self.ema[0] and self.rsi[0] < 40 and self.position.size >= 0:
            self.order = self.close(exectype=bt.Order.Close)  # Close any existing long positions
            self.order = self.sell(size=10, exectype=bt.Order.Close)
            print(f"Short Price: {self.data.close[0]} - {dt} - {self.position.size}")
        else:
            # Optional: Define an exit strategy if needed
            pass


        if self.position.size > 0:
            ShortOrLong = "Long Position Open"
        elif self.position.size < 0:
            ShortOrLong = "Short Position Open"
        elif self.position.size == 0:
            ShortOrLong = "No Trades Open"


        print(f"{dt} - Close Price: {close_price} - {ShortOrLong} - {self.position.size} - RSI Value: {self.rsi[0]} - SMA Value : {self.ema[0]}")  # Print datetime & close price

    def notify_order(self, order):
        """ Track executed orders """
        if order.status in [bt.Order.Completed]:
            exec_price = order.executed.price
            dt = self.datas[0].datetime.datetime(0)
            print(f"{dt} - ORDER EXECUTED at {exec_price}, Size: {order.executed.size}")
        elif order.status in [bt.Order.Canceled, bt.Order.Margin, bt.Order.Rejected]:
            print("Order Canceled/Rejected")
        self.order = None  # Reset order tracking