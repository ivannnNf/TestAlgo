import decimal
import backtrader
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from strategy import RSIEMAStrategy as RS
import numpy as np

cerebro = backtrader.Cerebro()
cerebro.broker.setcash(100000.0)

data = backtrader.feeds.YahooFinanceCSVData(
    dataname='INDEX_ETHUSD, 1D.csv',
    reverse=False,
    adjclose=False,
    decimals=4,
    todate=datetime.datetime(2025, 2, 9)
)

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
print('Net Profit: %.2f' % net_profit)
print(cerebro.broker.get_cash())

# Plotting the results
cerebro.plot()

# Plotting the additional performance metrics
years = range(cerebro.datas[0].datetime.date(0).year, cerebro.datas[0].datetime.date(-1).year + 1)
returns = [total_return / len(years)] * len(years)

# plt.figure(figsize=(10, 5))
# plt.xlabel('Time')
# plt.ylabel('Position Size')
# plt.title('Position Sizes Over Time')
# plt.legend()
# Assuming plot_strategy is an instance of a strategy class
# plot_strategy = RS()  # Ensure this line is executed before plotting
# plt.plot(plot_strategy.position_sizes, label='Position Size')
# plt.show()

# Plotting balance equity vs number of trades

closed_positions = np.cumsum(strategy_instance.closed_positions)
trade_numbers = list(range(1, len(closed_positions) + 1))
daily_returns = np.diff(closed_positions) / closed_positions[:-1] if len(closed_positions) > 1 else []



# Plotting the results
plt.figure(figsize=(14, 7))
plt.plot(trade_numbers, closed_positions, label='Closed Positions')
plt.title('Closed Positions Over Number of Trades')
plt.xlabel('Number of Trades')
plt.ylabel('Closed Positions')
plt.legend()
plt.tight_layout()
plt.show()
