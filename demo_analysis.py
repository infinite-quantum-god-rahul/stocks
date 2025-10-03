import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

class DemoStockAnalyzer:
    def __init__(self):
        self.results = []
        
    def get_sample_stocks(self):
        """Get a sample of major Nifty 500 stocks for demonstration"""
        sample_stocks = {
            'RELIANCE.NS': 'Large Cap',
            'TCS.NS': 'Large Cap', 
            'HDFCBANK.NS': 'Large Cap',
            'INFY.NS': 'Large Cap',
            'HINDUNILVR.NS': 'Large Cap',
            'ITC.NS': 'Large Cap',
            'SBIN.NS': 'Large Cap',
            'BHARTIARTL.NS': 'Large Cap',
            'KOTAKBANK.NS': 'Large Cap',
            'LT.NS': 'Large Cap',
            'ASIANPAINT.NS': 'Large Cap',
            'AXISBANK.NS': 'Large Cap',
            'MARUTI.NS': 'Large Cap',
            'SUNPHARMA.NS': 'Large Cap',
            'ULTRACEMCO.NS': 'Large Cap',
            'WIPRO.NS': 'Large Cap',
            'NESTLEIND.NS': 'Large Cap',
            'TITAN.NS': 'Large Cap',
            'POWERGRID.NS': 'Large Cap',
            'NTPC.NS': 'Large Cap',
            'TATAMOTORS.NS': 'Mid Cap',
            'JSWSTEEL.NS': 'Mid Cap',
            'ADANIPORTS.NS': 'Mid Cap',
            'GRASIM.NS': 'Mid Cap',
            'CIPLA.NS': 'Mid Cap'
        }
        
        print(f"Using sample of {len(sample_stocks)} major Nifty 500 stocks for demonstration")
        return sample_stocks
    
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
    
    def fetch_stock_data(self, symbol, years=15):
        """Fetch monthly stock data for the specified number of years"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years * 365)
            
            print(f"  Fetching data for {symbol}...")
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date, interval='1mo')
            
            if data.empty:
                print(f"  No data available for {symbol}")
                return None
                
            # Calculate Heikin Ashi
            data = self.calculate_heikin_ashi(data)
            
            # Calculate 89 EMA on Heikin Ashi close
            data['EMA_89'] = self.calculate_ema(data['HA_Close'], 89)
            
            print(f"  Successfully processed {len(data)} monthly candles for {symbol}")
            return data
            
        except Exception as e:
            print(f"  Error fetching data for {symbol}: {e}")
            return None
    
    def analyze_stock(self, symbol, market_cap):
        """Analyze a single stock for signals"""
        print(f"Analyzing {symbol} ({market_cap})...")
        
        data = self.fetch_stock_data(symbol)
        if data is None or len(data) < 90:  # Need at least 89 periods for EMA
            print(f"  Skipping {symbol} - insufficient data")
            return
        
        # Find signals where Heikin Ashi close is above 89 EMA
        signals = data[data['HA_Close'] > data['EMA_89']].copy()
        
        if not signals.empty:
            print(f"  Found {len(signals)} signals for {symbol}")
            for date, row in signals.iterrows():
                self.results.append({
                    'Date': date.strftime('%Y-%m-%d'),
                    'Stock_Ticker': symbol.replace('.NS', ''),
                    'Market_Cap': market_cap,
                    'HA_Close': round(row['HA_Close'], 2),
                    'EMA_89': round(row['EMA_89'], 2)
                })
        else:
            print(f"  No signals found for {symbol}")
        
        time.sleep(1)  # Rate limiting
    
    def run_analysis(self):
        """Run the complete analysis"""
        print("Nifty 500 EMA 89 Analysis with Heikin Ashi Candlesticks")
        print("=" * 70)
        print("Monthly Timeframe | Past 15 Years | Heikin Ashi Candlesticks")
        print("=" * 70)
        
        # Get sample stock list
        stocks = self.get_sample_stocks()
        
        # Analyze each stock
        for symbol, market_cap in stocks.items():
            self.analyze_stock(symbol, market_cap)
            print("-" * 50)
        
        # Convert results to DataFrame and sort by date
        results_df = pd.DataFrame(self.results)
        if not results_df.empty:
            results_df = results_df.sort_values('Date', ascending=False)
            
            print(f"\nAnalysis Complete! Found {len(results_df)} signals.")
            print("=" * 70)
            print("Recent Signals (Last 20):")
            print("=" * 70)
            print(results_df[['Date', 'Stock_Ticker', 'Market_Cap']].head(20).to_string(index=False))
            
            # Save to CSV
            results_df.to_csv('nifty500_ema89_demo_results.csv', index=False)
            print(f"\nResults saved to 'nifty500_ema89_demo_results.csv'")
            
            # Summary by market cap
            print("\nSummary by Market Cap:")
            print("=" * 30)
            summary = results_df.groupby('Market_Cap').size().reset_index(name='Signal_Count')
            print(summary.to_string(index=False))
            
            # Show sample of detailed results
            print("\nSample Detailed Results:")
            print("=" * 50)
            sample_detailed = results_df.head(10)[['Date', 'Stock_Ticker', 'Market_Cap', 'HA_Close', 'EMA_89']]
            print(sample_detailed.to_string(index=False))
            
        else:
            print("No signals found in the analysis period.")
        
        return results_df

if __name__ == "__main__":
    analyzer = DemoStockAnalyzer()
    results = analyzer.run_analysis()
