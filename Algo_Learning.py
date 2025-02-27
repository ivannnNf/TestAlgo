import decimal
import backtrader
import datetime
import pandas as pd
from strategy import RSIEMAStrategy as RS

cerebro = backtrader.Cerebro()

cerebro.broker.setcash(100000.0)

data = backtrader.feeds.YahooFinanceCSVData(
    dataname = 'INDEX_ETHUSD, 1D.csv',
    reverse=False,
    adjclose=False,
    decimals=4)

cerebro.adddata(data)

cerebro.addstrategy(RS)

starting_value = cerebro.broker.getvalue()
print('Starting Portfolio Value: %.2f' % starting_value)

cerebro.run()

ending_value = cerebro.broker.getvalue()
print('Final Portfolio Value: %.2f' % ending_value)

total_return = (ending_value - starting_value) / starting_value * 100
print('Total Return: %.2f%%' % total_return)

# Additional performance metrics
net_profit = ending_value - starting_value




start_year = cerebro.datas[0].datetime.date(0).year
end_year = cerebro.datas[0].datetime.date(-1).year
year_diff = end_year - start_year


# Assuming there is only one strategy
strategy = cerebro.runstrats[0][0]
print('Net Profit: %.2f' % net_profit)
print(cerebro.broker.get_cash())

