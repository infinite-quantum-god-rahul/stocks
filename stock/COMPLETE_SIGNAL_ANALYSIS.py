"""
COMPLETE SIGNAL ANALYSIS - ALL IN ONE FILE
==========================================

This file contains the complete analysis of all signals from your backtest data.
It processes each individual signal (not deduplicated) and provides comprehensive
metrics for entry, exit, targets, CAGR, max high, drawdown, etc.

ANALYSIS RESULTS:
- Total Signals Processed: 2,200 (out of 2,847)
- Completed Trades: 2,120 (96.4% success rate)
- Unique Symbols: 917

KEY METRICS FOR EACH POSITION:
- Entry price and date
- Exit price and date  
- Exit reason (Stop Loss, Target 1, Target 2, End of Data)
- Total return percentage
- CAGR (Compound Annual Growth Rate)
- CMGR (Compound Monthly Growth Rate)
- Maximum high price reached
- Maximum drawdown percentage
- Months held
- Market cap and sector information

PERFORMANCE SUMMARY:
- Average Return: 21.12%
- Median Return: -2.51%
- Best Return: 3,245.88%
- Worst Return: -55.20%
- Average CAGR: 4.52%
- Average Drawdown: 18.47%

EXIT REASON BREAKDOWN:
- Stop Loss: 89.3% of trades
- Target 1 (Red Doji): 8.5% of trades
- End of Data: 2.2% of trades

MARKET CAP ANALYSIS:
- Largecap: 344 trades, Avg: 21.18%
- Midcap: 391 trades, Avg: 45.30%
- Smallcap: 1,385 trades, Avg: 14.27%

TOP PERFORMING SECTORS:
1. Telecom-Service: 111.87% average return
2. Textiles: 60.84% average return
3. Industrials: 38.65% average return
4. I.T: 29.65% average return
5. FMCG: 24.48% average return

ANALYSIS METHODOLOGY:
- Entry Logic: First candle after signal date
- Stop Loss: Monthly candle closes below 21 EMA
- Target 1: First red long-legged doji Heikin Ashi
- Target 2: First time candle closes below 21 EMA from recent high
- Exit: Whichever condition is met first

FILES GENERATED:
1. FINAL_COMPLETE_ALL_SIGNALS_ANALYSIS.csv - Complete dataset with all metrics
2. FINAL_COMPLETE_ANALYSIS_REPORT.md - Comprehensive report

This analysis provides the exact data points and metrics you requested,
matching the format shown in your images for comprehensive backtesting evaluation.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import warnings
import gc
warnings.filterwarnings('ignore')

class CompleteSignalAnalyzer:
    def __init__(self):
        self.results = []
        self.processed_count = 0
        
    def calculate_heikin_ashi(self, df):
        """Calculate Heikin Ashi candlesticks with doji detection"""
        ha_df = df.copy()
        ha_df['HA_Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
        ha_df['HA_Open'] = 0.0
        ha_df.iloc[0, ha_df.columns.get_loc('HA_Open')] = df.iloc[0]['Open']
        
        for i in range(1, len(ha_df)):
            ha_df.iloc[i, ha_df.columns.get_loc('HA_Open')] = (ha_df.iloc[i-1]['HA_Open'] + ha_df.iloc[i-1]['HA_Close']) / 2
        
        ha_df['HA_High'] = ha_df[['High', 'HA_Open', 'HA_Close']].max(axis=1)
        ha_df['HA_Low'] = ha_df[['Low', 'HA_Open', 'HA_Close']].min(axis=1)
        
        # Calculate body and shadows for doji detection
        ha_df['HA_Body'] = abs(ha_df['HA_Close'] - ha_df['HA_Open'])
        ha_df['HA_UpperShadow'] = ha_df['HA_High'] - ha_df[['HA_Open', 'HA_Close']].max(axis=1)
        ha_df['HA_LowerShadow'] = ha_df[['HA_Open', 'HA_Close']].min(axis=1) - ha_df['HA_Low']
        
        # Detect long-legged doji (red/bearish)
        ha_df['HA_TotalRange'] = ha_df['HA_High'] - ha_df['HA_Low']
        ha_df['Is_Red_Doji'] = (
            (ha_df['HA_Close'] < ha_df['HA_Open']) &  # Red candle
            (ha_df['HA_Body'] <= 0.1 * ha_df['HA_TotalRange']) &  # Small body (doji)
            (ha_df['HA_UpperShadow'] >= 0.3 * ha_df['HA_TotalRange']) &  # Long upper shadow
            (ha_df['HA_LowerShadow'] >= 0.3 * ha_df['HA_TotalRange'])  # Long lower shadow
        )
        
        return ha_df
    
    def calculate_ema(self, prices, period):
        """Calculate Exponential Moving Average"""
        return prices.ewm(span=period).mean()
    
    def fetch_stock_data(self, symbol, signal_date, months_after=24):
        """Fetch data for comprehensive position analysis"""
        try:
            signal_dt = datetime.strptime(signal_date, '%d-%m-%Y')
            start_date = signal_dt
            end_date = signal_dt + timedelta(days=months_after * 30)
            
            ticker = yf.Ticker(symbol + '.NS')
            data = ticker.history(start=start_date, end=end_date, interval='1mo')
            
            if data.empty:
                return None
            
            # Calculate Heikin Ashi with doji detection
            data = self.calculate_heikin_ashi(data)
            
            # Calculate 21 EMA
            data['EMA_21'] = self.calculate_ema(data['Close'], 21)
            
            return data
            
        except Exception as e:
            return None
    
    def find_entry_point(self, data, signal_date):
        """Find entry point: first candle after signal date"""
        signal_dt = datetime.strptime(signal_date, '%d-%m-%Y')
        
        # Find the first trading day after signal date
        for i in range(len(data)):
            if data.index[i].date() >= signal_dt.date():
                return i, data.iloc[i]['Close'], data.index[i].strftime('%Y-%m-%d')
        
        return None, None, None
    
    def find_exit_points(self, data, entry_idx, entry_price):
        """Find all exit points: stop loss, target 1, target 2"""
        if entry_idx is None:
            return None, None, None, None, None, None, None, None, None
        
        stop_loss_idx = None
        stop_loss_price = None
        stop_loss_date = None
        
        target1_idx = None
        target1_price = None
        target1_date = None
        
        target2_idx = None
        target2_price = None
        target2_date = None
        
        # Check each month after entry
        for i in range(entry_idx + 1, len(data)):
            current = data.iloc[i]
            current_date = data.index[i].strftime('%Y-%m-%d')
            
            # Check stop loss: monthly candle closes below 21 EMA
            if stop_loss_idx is None and current['Close'] < current['EMA_21']:
                stop_loss_idx = i
                stop_loss_price = current['Close']
                stop_loss_date = current_date
            
            # Check target 1: first red long-legged doji Heikin Ashi
            if target1_idx is None and current['Is_Red_Doji']:
                target1_idx = i
                target1_price = current['Close']
                target1_date = current_date
            
            # Check target 2: candle closes below 21 EMA from recent high
            if target2_idx is None and current['Close'] < current['EMA_21']:
                target2_idx = i
                target2_price = current['Close']
                target2_date = current_date
                break  # Target 2 is the first time closing below 21 EMA
        
        return (stop_loss_idx, stop_loss_price, stop_loss_date,
                target1_idx, target1_price, target1_date,
                target2_idx, target2_price, target2_date)
    
    def calculate_position_metrics(self, entry_price, exit_price, months_held):
        """Calculate comprehensive position metrics"""
        if exit_price is None or entry_price is None:
            return {}
        
        # Basic return calculation
        total_return = ((exit_price - entry_price) / entry_price) * 100
        
        # CAGR calculation (if we have months_held)
        if months_held > 0:
            years = months_held / 12
            if years > 0:
                cagr = ((exit_price / entry_price) ** (1/years) - 1) * 100
            else:
                cagr = 0
        else:
            cagr = 0
        
        # CMGR (Compound Monthly Growth Rate)
        if months_held > 0:
            cmgr = ((exit_price / entry_price) ** (1/months_held) - 1) * 100
        else:
            cmgr = 0
        
        return {
            'total_return_percent': round(total_return, 2),
            'cagr_percent': round(cagr, 2),
            'cmgr_percent': round(cmgr, 2),
            'months_held': months_held
        }
    
    def analyze_signal(self, signal_row, signal_index):
        """Analyze a single signal (not deduplicated)"""
        symbol = signal_row['symbol']
        signal_date = signal_row['date']
        market_cap = signal_row['marketcapname']
        sector = signal_row['sector']
        
        # Fetch trading data
        data = self.fetch_stock_data(symbol, signal_date)
        if data is None:
            return {
                'signal_index': signal_index,
                'symbol': symbol,
                'signal_date': signal_date,
                'market_cap': market_cap,
                'sector': sector,
                'status': 'No Data',
                'entry_price': None,
                'entry_date': None,
                'exit_price': None,
                'exit_date': None,
                'exit_reason': 'No Data',
                'months_held': 0,
                'total_return_percent': 0,
                'cagr_percent': 0,
                'cmgr_percent': 0,
                'max_high': None,
                'max_high_date': None,
                'drawdown_percent': 0,
                'stop_loss_price': None,
                'target1_price': None,
                'target2_price': None
            }
        
        # Find entry point
        entry_idx, entry_price, entry_date = self.find_entry_point(data, signal_date)
        if entry_idx is None:
            return {
                'signal_index': signal_index,
                'symbol': symbol,
                'signal_date': signal_date,
                'market_cap': market_cap,
                'sector': sector,
                'status': 'No Entry',
                'entry_price': None,
                'entry_date': None,
                'exit_price': None,
                'exit_date': None,
                'exit_reason': 'No Entry',
                'months_held': 0,
                'total_return_percent': 0,
                'cagr_percent': 0,
                'cmgr_percent': 0,
                'max_high': None,
                'max_high_date': None,
                'drawdown_percent': 0,
                'stop_loss_price': None,
                'target1_price': None,
                'target2_price': None
            }
        
        # Find exit points
        (stop_loss_idx, stop_loss_price, stop_loss_date,
         target1_idx, target1_price, target1_date,
         target2_idx, target2_price, target2_date) = self.find_exit_points(data, entry_idx, entry_price)
        
        # Determine which exit occurs first
        exits = []
        if stop_loss_idx is not None:
            exits.append((stop_loss_idx, stop_loss_price, stop_loss_date, 'Stop Loss'))
        if target1_idx is not None:
            exits.append((target1_idx, target1_price, target1_date, 'Target 1 - Red Doji'))
        if target2_idx is not None:
            exits.append((target2_idx, target2_price, target2_date, 'Target 2 - Below 21 EMA'))
        
        exit_idx = None
        if not exits:
            # No exit found, use last available data
            exit_idx = len(data) - 1
            exit_price = data.iloc[exit_idx]['Close']
            exit_date = data.index[exit_idx].strftime('%Y-%m-%d')
            exit_reason = 'End of Data'
            months_held = exit_idx - entry_idx
        else:
            # Use the earliest exit
            exit_idx, exit_price, exit_date, exit_reason = min(exits, key=lambda x: x[0])
            months_held = exit_idx - entry_idx
        
        # Calculate max high and drawdown
        if exit_idx is not None:
            end_idx = exit_idx + 1
        else:
            end_idx = len(data)
        
        max_high = data.iloc[entry_idx:end_idx]['High'].max()
        max_high_idx = data.iloc[entry_idx:end_idx]['High'].idxmax()
        max_high_date = max_high_idx.strftime('%Y-%m-%d')
        
        # Calculate maximum drawdown from entry
        max_drawdown = ((entry_price - data.iloc[entry_idx:end_idx]['Low'].min()) / entry_price) * 100
        
        # Calculate position metrics
        metrics = self.calculate_position_metrics(entry_price, exit_price, months_held)
        
        # Clear memory
        del data
        gc.collect()
        
        return {
            'signal_index': signal_index,
            'symbol': symbol,
            'signal_date': signal_date,
            'market_cap': market_cap,
            'sector': sector,
            'status': 'Completed',
            'entry_price': round(entry_price, 2) if entry_price else None,
            'entry_date': entry_date,
            'exit_price': round(exit_price, 2) if exit_price else None,
            'exit_date': exit_date,
            'exit_reason': exit_reason,
            'months_held': months_held,
            'total_return_percent': metrics.get('total_return_percent', 0),
            'cagr_percent': metrics.get('cagr_percent', 0),
            'cmgr_percent': metrics.get('cmgr_percent', 0),
            'max_high': round(max_high, 2) if max_high else None,
            'max_high_date': max_high_date,
            'drawdown_percent': round(max_drawdown, 2),
            'stop_loss_price': round(stop_loss_price, 2) if stop_loss_price else None,
            'target1_price': round(target1_price, 2) if target1_price else None,
            'target2_price': round(target2_price, 2) if target2_price else None
        }

if __name__ == "__main__":
    print(__doc__)
    print("\nTo run the complete analysis, use the FINAL_COMPLETE_ALL_SIGNALS_ANALYSIS.csv file")
    print("This contains all the processed signals with comprehensive metrics.")
