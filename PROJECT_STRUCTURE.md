# Project Structure - Nifty 500 EMA Analysis

## Repository: https://github.com/infinite-quantum-god-rahul/stocks.git

### Files Overview

#### Core Analysis Scripts
- **`demo_analysis.py`** - Working demonstration script with 25 major Nifty 500 stocks
- **`nifty500_ema_analysis.py`** - Full-scale analysis script for complete Nifty 500 list
- **`nifty500_scraper.py`** - Module to fetch Nifty 500 stock list from NSE

#### Configuration & Dependencies
- **`requirements.txt`** - Python package dependencies
- **`README.md`** - Project documentation and usage instructions

#### Results
- **`nifty500_ema89_demo_results.csv`** - Sample analysis results (3,830 signals)

### Analysis Features

#### Technical Analysis
- **Heikin Ashi Candlesticks**: Smoothed candlestick calculation
- **89-period EMA**: Long-term trend indicator
- **Monthly Timeframe**: 15 years of historical data
- **Signal Detection**: HA Close > 89 EMA

#### Stock Classification
- **Large Cap**: Major companies (RELIANCE, TCS, HDFCBANK, etc.)
- **Mid Cap**: Medium-sized companies (TATAMOTORS, JSWSTEEL, etc.)
- **Small Cap**: Smaller companies (classified automatically)

#### Data Sources
- **Yahoo Finance**: Historical stock data via yfinance
- **NSE**: Stock list and market data
- **Real-time**: Live market data fetching

### Usage Instructions

#### Quick Start (Demo)
```bash
pip install -r requirements.txt
python demo_analysis.py
```

#### Full Analysis
```bash
python nifty500_ema_analysis.py
```

### Results Format
```
Date        | Stock_Ticker | Market_Cap | HA_Close | EMA_89
2025-10-01  | CIPLA       | Mid Cap    | 1514.85  | 1070.29
2025-10-01  | SBIN        | Large Cap  | 869.61   | 540.05
```

### Key Statistics
- **Total Signals**: 3,830 instances
- **Large Cap Signals**: 3,099 (81%)
- **Mid Cap Signals**: 731 (19%)
- **Analysis Period**: 15 years (180 monthly candles per stock)
- **Sample Stocks**: 25 major Nifty 500 stocks analyzed

### Technical Implementation
- **Heikin Ashi Formula**: HA_Close = (O + H + L + C) / 4
- **EMA Calculation**: Exponential Moving Average with 89-period span
- **Rate Limiting**: Built-in delays to respect API limits
- **Error Handling**: Robust error handling for data fetching issues

### Future Enhancements
- Complete Nifty 500 analysis
- Real-time signal alerts
- Portfolio optimization features
- Additional technical indicators
- Web dashboard interface
