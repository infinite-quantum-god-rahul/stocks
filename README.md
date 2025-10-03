# Nifty 500 EMA 89 Analysis with Heikin Ashi Candlesticks

This script analyzes Nifty 500 stocks to find instances where the stock closed above its 89-period Exponential Moving Average (EMA) using Heikin Ashi candlesticks on monthly timeframe for the past 15 years.

## Features

- Fetches Nifty 500 stock list from NSE
- Calculates Heikin Ashi candlesticks
- Computes 89-period EMA on Heikin Ashi close prices
- Identifies signals where Heikin Ashi close > 89 EMA
- Classifies stocks by market cap (Large/Mid/Small)
- Exports results to CSV with date, ticker, and market cap

## Requirements

Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the main analysis script:

```bash
python nifty500_ema_analysis.py
```

## Output

The script will:
1. Fetch Nifty 500 stock list
2. Download monthly data for each stock (past 15 years)
3. Calculate Heikin Ashi candlesticks
4. Compute 89 EMA
5. Identify signals and display results
6. Save results to `nifty500_ema89_signals.csv`

## Results Format

The output CSV contains:
- Date: Date of the signal
- Stock_Ticker: Stock symbol (without .NS suffix)
- Market_Cap: Large Cap / Mid Cap / Small Cap classification
- HA_Close: Heikin Ashi close price
- EMA_89: 89-period EMA value

## Note

- Uses monthly timeframe as requested
- Heikin Ashi candlesticks are calculated from OHLC data
- Market cap classification is based on typical NSE classifications
- Rate limiting is applied to avoid overwhelming the data provider
