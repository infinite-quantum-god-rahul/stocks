import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class ComprehensiveDebugger:
    def __init__(self):
        pass
    
    def calculate_heikin_ashi(self, df):
        """Calculate Heikin Ashi candlesticks"""
        ha_df = df.copy()
        
        # Heikin Ashi Close = (Open + High + Low + Close) / 4
        ha_df['HA_Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
        
        # Heikin Ashi Open = (Previous HA Open + Previous HA Close) / 2
        ha_df['HA_Open'] = 0.0
        ha_df.iloc[0, ha_df.columns.get_loc('HA_Open')] = df.iloc[0]['Open']
        
        for i in range(1, len(ha_df)):
            ha_df.iloc[i, ha_df.columns.get_loc('HA_Open')] = (ha_df.iloc[i-1]['HA_Open'] + ha_df.iloc[i-1]['HA_Close']) / 2
        
        # Heikin Ashi High = max(High, HA_Open, HA_Close)
        ha_df['HA_High'] = ha_df[['High', 'HA_Open', 'HA_Close']].max(axis=1)
        
        # Heikin Ashi Low = min(Low, HA_Open, HA_Close)
        ha_df['HA_Low'] = ha_df[['Low', 'HA_Open', 'HA_Close']].min(axis=1)
        
        return ha_df
    
    def calculate_ema(self, prices, period):
        """Calculate Exponential Moving Average"""
        return prices.ewm(span=period).mean()
    
    def debug_stock_signals(self, symbol, target_dates):
        """Debug specific signals for a stock"""
        print(f"=== DEBUGGING {symbol} SIGNALS ===")
        
        # Fetch data with extended range for EMA calculation
        end_date = datetime.now()
        start_date = end_date - timedelta(days=15 * 365)
        
        ticker = yf.Ticker(symbol)
        data = ticker.history(start=start_date, end=end_date, interval='1mo')
        
        if data.empty:
            print(f"No data available for {symbol}")
            return
        
        # Calculate Heikin Ashi
        data = self.calculate_heikin_ashi(data)
        
        # Calculate 89 EMA on HA_Close
        data['EMA_89_HA'] = self.calculate_ema(data['HA_Close'], 89)
        
        print(f"Total data points: {len(data)}")
        print(f"EMA starts from index: {89}")
        
        # Check each target date
        for target_date in target_dates:
            print(f"\n--- Checking {target_date} ---")
            
            # Find the closest date
            closest_date = None
            min_diff = float('inf')
            
            for date in data.index:
                # Convert to naive datetime for comparison
                date_naive = date.to_pydatetime().replace(tzinfo=None)
                diff = abs((date_naive - target_date).days)
                if diff < min_diff:
                    min_diff = diff
                    closest_date = date
            
            if closest_date is None:
                print(f"Date {target_date} not found in data")
                continue
            
            # Get data for that date and surrounding dates
            date_idx = data.index.get_loc(closest_date)
            
            if date_idx < 90:  # Need at least 89 months for EMA
                print(f"Not enough data for EMA calculation at {closest_date}")
                continue
            
            current = data.iloc[date_idx]
            one_month_ago = data.iloc[date_idx - 1]
            
            print(f"Date: {closest_date.strftime('%Y-%m-%d')}")
            print(f"HA_Close: {current['HA_Close']:.2f}")
            print(f"HA_Open: {current['HA_Open']:.2f}")
            print(f"EMA_89_HA: {current['EMA_89_HA']:.2f}")
            print(f"Regular_Close: {current['Close']:.2f}")
            
            # Check conditions
            cond1 = current['HA_Close'] > current['HA_Open']
            cond2 = current['HA_Close'] > current['EMA_89_HA']
            cond3 = current['HA_Open'] <= current['EMA_89_HA']
            cond5 = one_month_ago['HA_Close'] < one_month_ago['EMA_89_HA']
            
            print(f"Condition 1 (HA_Close > HA_Open): {cond1}")
            print(f"Condition 2 (HA_Close > EMA89): {cond2}")
            print(f"Condition 3 (HA_Open <= EMA89): {cond3}")
            print(f"Condition 5 (Prev HA_Close < Prev EMA89): {cond5}")
            
            signal = cond1 and cond2 and cond3 and cond5
            print(f"OVERALL SIGNAL: {signal}")
            
            # Show previous month for context
            print(f"Previous month ({one_month_ago.name.strftime('%Y-%m-%d')}):")
            print(f"  HA_Close: {one_month_ago['HA_Close']:.2f}")
            print(f"  EMA_89_HA: {one_month_ago['EMA_89_HA']:.2f}")
            
            # Show crossover analysis
            if date_idx >= 1:
                prev = data.iloc[date_idx - 1]
                crossover = (prev['HA_Close'] <= prev['EMA_89_HA'] and 
                           current['HA_Close'] > current['EMA_89_HA'])
                print(f"Crossed above EMA this month: {crossover}")

def main():
    debugger = ComprehensiveDebugger()
    
    # Debug ITC signals
    itc_dates = [
        datetime(2021, 3, 1),
        datetime(2021, 8, 1),
        datetime(2021, 9, 1)  # The actual crossover date from chart
    ]
    
    debugger.debug_stock_signals('ITC.NS', itc_dates)
    
    print("\n" + "="*80)
    
    # Debug NTPC signals
    ntpc_dates = [
        datetime(2021, 3, 1),
        datetime(2021, 5, 1)
    ]
    
    debugger.debug_stock_signals('NTPC.NS', ntpc_dates)

if __name__ == "__main__":
    main()
