import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# My choice of 5 Nifty 50 stocks
companies = ['MARUTI.NS', 'TITAN.NS', 'TATASTEEL.NS', 'NESTLEIND.NS', 'LT.NS']
tix = yf.Tickers(companies)

# Setting the date range
endate = datetime.now().strftime('%Y-%m-%d')
tixh = tix.history(start='2024-03-02', end=endate)

# Daily % change and 20-day moving average
dailychange = tixh['Close'].pct_change()
mvavg = tixh['Close'].rolling(window=20).mean()

# Plot closing prices with moving averages
plt.figure(figsize=(14, 8))
for company in companies:
    plt.plot(tixh['Close'][company], label=f'{company} Close Price')
    plt.plot(mvavg[company], label=f'{company} 20-Day MA', linestyle='--')
plt.title('Closing Prices with 20-Day Moving Average')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# Fetching historical stock data for TITAN.NS
company = 'TITAN.NS'
stock_data = yf.download(company, start='2023-06-01', end='2024-08-01')

# Calculate 50-day and 200-day Simple Moving Averages (SMA)
stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()

# Create a signal column (1 for buy, 0 for sell)
stock_data['Signal'] = np.where(stock_data['SMA_50'] > stock_data['SMA_200'], 1, 0)
stock_data['Position'] = stock_data['Signal'].diff()

# Plot the stock price with buy/sell signals
plt.figure(figsize=(14, 8))
plt.plot(stock_data['Close'], label='Close Price', alpha=0.35)
plt.plot(stock_data['SMA_50'], label='50-Day SMA', alpha=0.75)
plt.plot(stock_data['SMA_200'], label='200-Day SMA', alpha=0.75)

# Buy/Sell signals
plt.plot(stock_data[stock_data['Position'] == 1].index, 
         stock_data['SMA_50'][stock_data['Position'] == 1], 
         '^', markersize=10, color='g', lw=0, label='Buy Signal')
plt.plot(stock_data[stock_data['Position'] == -1].index, 
         stock_data['SMA_50'][stock_data['Position'] == -1], 
         'v', markersize=10, color='r', lw=0, label='Sell Signal')

plt.title(f'Moving Average Crossover Strategy for {company}')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# Calculate cumulative returns
stock_data['Market_Returns'] = stock_data['Close'].pct_change()
stock_data['Strategy_Returns'] = stock_data['Market_Returns'] * stock_data['Position'].shift(1)
stock_data['Cumulative_Market_Returns'] = (1 + stock_data['Market_Returns']).cumprod() - 1
stock_data['Cumulative_Strategy_Returns'] = (1 + stock_data['Strategy_Returns']).cumprod() - 1

# Plot cumulative returns comparison
plt.figure(figsize=(14, 7))
plt.plot(stock_data['Cumulative_Market_Returns'], label='Cumulative Market Returns', alpha=0.7)
plt.plot(stock_data['Cumulative_Strategy_Returns'], label='Cumulative Strategy Returns', alpha=0.7)
plt.title('Cumulative Returns Comparison')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.legend()
plt.grid()
plt.show()

# Final return values
final_market_return = stock_data['Cumulative_Market_Returns'].iloc[-1]
final_strategy_return = stock_data['Cumulative_Strategy_Returns'].iloc[-1]
print(f"Final Cumulative Market Return: {final_market_return:.2%}")
print(f"Final Cumulative Strategy Return: {final_strategy_return:.2%}")

# Stop-loss implementation (5% SL)
stop_loss_percentage = 0.05
stock_data['Cumulative_Strategy_Returns_SL'] = 0
holding = False
entry_price = 0

for i in range(len(stock_data)):
    if stock_data['Position'].iloc[i] == 1:  # Buy signal
        entry_price = stock_data['Close'].iloc[i]
        holding = True
    elif holding:  # Stop-loss check
        if stock_data['Close'].iloc[i] < entry_price * (1 - stop_loss_percentage):
            stock_data['Cumulative_Strategy_Returns_SL'].iloc[i] = (stock_data['Close'].iloc[i] / entry_price) - 1
            holding = False
        else:
            stock_data['Cumulative_Strategy_Returns_SL'].iloc[i] = (stock_data['Close'].iloc[i] / entry_price) - 1

# Plot Stop-Loss Strategy Results
plt.figure(figsize=(14, 8))
plt.plot(stock_data['Cumulative_Strategy_Returns_SL'], label='Strategy with Stop-Loss', color='orange')
plt.title(f'Stop-Loss Strategy for {company}')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.legend()
plt.grid()
plt.show()

# Final return with stop-loss
print(f'Final Strategy Return with Stop-Loss: {stock_data["Cumulative_Strategy_Returns_SL"].iloc[-1] * 100:.2f}%')