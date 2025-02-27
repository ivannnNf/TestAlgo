# Create a Strategy


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
        ('ema_period', 20),
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI(period=self.params.rsi_period)
        self.ema = bt.indicators.EMA(period=self.params.ema_period)
    
    def next(self):
        if not self.position:  # Check if no open position
            if self.data.close[0] > self.ema[0] and self.rsi[0] > 60 and not self.position.size > 0 :
                self.close
                self.buy(size=100)

            elif self.data.close[0] < self.ema[0] and self.rsi[0] < 40 and not self.position.size < 0:
                self.close()
                self.sell(size=100)
        else:
            # Optional: Define an exit strategy if needed
            pass