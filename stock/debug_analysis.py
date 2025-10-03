import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def debug_itc_signals():
    """Debug ITC signals to understand the discrepancy"""
    
    print("=== DEBUGGING ITC SIGNALS ===")
    
    # Fetch ITC data
    ticker = yf.Ticker('ITC.NS')
    data = ticker.history(start='2020-01-01', end='2022-01-01', interval='1mo')
    
    # Calculate Heikin Ashi
    def calculate_heikin_ashi(df):
        ha_df = df.copy()
        ha_df['HA_Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
        ha_df['HA_Open'] = 0.0
        ha_df.iloc[0, ha_df.columns.get_loc('HA_Open')] = df.iloc[0]['Open']
        
        for i in range(1, len(ha_df)):
            ha_df.iloc[i, ha_df.columns.get_loc('HA_Open')] = (ha_df.iloc[i-1]['HA_Open'] + ha_df.iloc[i-1]['HA_Close']) / 2
        
        ha_df['HA_High'] = ha_df[['High', 'HA_Open', 'HA_Close']].max(axis=1)
        ha_df['HA_Low'] = ha_df[['Low', 'HA_Open', 'HA_Close']].min(axis=1)
        return ha_df
    
    data = calculate_heikin_ashi(data)
    
    # Calculate 89 EMA on HA_Close
    data['EMA_89_HA'] = data['HA_Close'].ewm(span=89).mean()
    
    # Filter for 2021 data
    data_2021 = data[(data.index >= '2021-01-01') & (data.index <= '2021-12-31')].copy()
    
    print("ITC 2021 Monthly Data:")
    print("=" * 80)
    
    for date, row in data_2021.iterrows():
        ha_close = row['HA_Close']
        ha_open = row['HA_Open']
        ema_89 = row['EMA_89_HA']
        
        # Check our conditions
        cond1 = ha_close > ha_open
        cond2 = ha_close > ema_89
        cond3 = ha_open <= ema_89
        
        # Check if previous month HA_Close was below EMA
        if date > data_2021.index[0]:
            prev_date = data_2021.index[data_2021.index.get_loc(date) - 1]
            prev_ha_close = data_2021.loc[prev_date, 'HA_Close']
            prev_ema_89 = data_2021.loc[prev_date, 'EMA_89_HA']
            cond5 = prev_ha_close < prev_ema_89
        else:
            cond5 = False
        
        signal = cond1 and cond2 and cond3 and cond5
        
        print(f"{date.strftime('%Y-%m-%d')}: HA_Close={ha_close:.2f}, HA_Open={ha_open:.2f}, EMA89={ema_89:.2f}")
        print(f"  Conditions: HA_Close>HA_Open={cond1}, HA_Close>EMA89={cond2}, HA_Open<=EMA89={cond3}, Prev_HA<Prev_EMA={cond5}")
        print(f"  SIGNAL: {signal}")
        print("-" * 60)
    
    # Also check the crossover point
    print("\n=== CROSSOVER ANALYSIS ===")
    print("Looking for HA_Close crossing above EMA_89...")
    
    for i in range(1, len(data_2021)):
        current = data_2021.iloc[i]
        previous = data_2021.iloc[i-1]
        
        if (previous['HA_Close'] <= previous['EMA_89_HA'] and 
            current['HA_Close'] > current['EMA_89_HA']):
            print(f"CROSSOVER FOUND: {data_2021.index[i].strftime('%Y-%m-%d')}")
            print(f"  Previous: HA_Close={previous['HA_Close']:.2f} <= EMA89={previous['EMA_89_HA']:.2f}")
            print(f"  Current:  HA_Close={current['HA_Close']:.2f} > EMA89={current['EMA_89_HA']:.2f}")

if __name__ == "__main__":
    debug_itc_signals()


