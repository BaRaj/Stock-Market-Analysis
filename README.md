# Stock Trading Strategy with Moving Averages and Stop-Loss
This project implements a stock trading strategy using moving average crossovers (50-day and 200-day Simple Moving Averages) and a stop-loss mechanism. It allows users to backtest the strategy on historical stock data and compare its performance to the market.

## Features
Simple Moving Average (SMA) Crossover Strategy: Generates buy/sell signals based on the crossover of short-term (50-day) and long-term (200-day) moving averages.
Stop-Loss Mechanism: Implements a stop-loss strategy with a configurable stop-loss percentage to limit downside risk.
Cumulative Return Comparison: Compares the performance of the strategy to hold the stock using cumulative return metrics.
Flexible Stock Selection: Easily customizable to test the strategy on any stock or group of stocks.
Visualization: Plots the stock's closing prices, moving averages, buy/sell signals, and cumulative returns.

## Requirements
To run this project, you will need the following Python packages:

yfinance – for fetching historical stock data.
pandas – for data manipulation and calculations.
numpy – for numerical operations.
matplotlib – for plotting graphs.

### You can install the required packages using:

Copy code
pip install yfinance pandas numpy matplotlib

## How to Use
### Clone the repository:

Copy code
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Modify stock tickers: Edit the companies list in the code to include the stock symbols you want to analyze. The default stocks are from the Nifty 50 index.

### Run the script: You can run the script in any Python environment:


Copy code
python stock_strategy.py
### Adjust parameters:
To change the stop-loss percentage, modify the stop_loss_percentage variable in the script.
You can also adjust the time for backtesting by editing the start and end dates in the yf.download() function.

## Outputs
Closing Prices & Moving Averages: The first plot shows the stock's closing prices along with its 50-day and 200-day moving averages.
Buy/Sell Signals: The second plot visualizes the points where buy or sell signals are triggered.
Cumulative Returns: The third plot compares the cumulative returns of the moving average strategy against the market returns.
Stop-Loss Performance: The final plot shows the performance of the strategy with a stop-loss mechanism applied.
