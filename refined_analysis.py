import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

class RefinedStockAnalyzer:
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
            'CIPLA.NS': 'Mid Cap',
            'ONGC.NS': 'Large Cap',
            'COALINDIA.NS': 'Large Cap',
            'TECHM.NS': 'Large Cap',
            'BAJFINANCE.NS': 'Large Cap',
            'ICICIBANK.NS': 'Large Cap'
        }
        
        print(f"Using sample of {len(sample_stocks)} major Nifty 500 stocks for refined analysis")
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
            
            # Calculate 89 EMA on Monthly Close (not HA_Close)
            data['EMA_89_Close'] = self.calculate_ema(data['Close'], 89)
            
            print(f"  Successfully processed {len(data)} monthly candles for {symbol}")
            return data
            
        except Exception as e:
            print(f"  Error fetching data for {symbol}: {e}")
            return None
    
    def check_refined_criteria(self, data, current_idx):
        """Check all refined criteria for a specific month"""
        if current_idx < 90:  # Need at least 89 months of data + 1 month ago
            return False, "Insufficient data"
        
        # Get current month data
        current = data.iloc[current_idx]
        
        # Get 1 month ago data
        one_month_ago = data.iloc[current_idx - 1]
        
        # Get 89 months ago data (for condition 4)
        if current_idx < 89:
            return False, "Insufficient data for 89 months ago check"
        eighty_nine_months_ago = data.iloc[current_idx - 89]
        
        criteria_results = []
        
        # Condition 1: Monthly HA-Close > Monthly HA-Open
        cond1 = current['HA_Close'] > current['HA_Open']
        criteria_results.append(f"HA_Close({current['HA_Close']:.2f}) > HA_Open({current['HA_Open']:.2f}): {cond1}")
        
        # Condition 2: Monthly HA-Close > Monthly EMA(Monthly Close, 89)
        cond2 = current['HA_Close'] > current['EMA_89_Close']
        criteria_results.append(f"HA_Close({current['HA_Close']:.2f}) > EMA89({current['EMA_89_Close']:.2f}): {cond2}")
        
        # Condition 3: Monthly HA-Open <= Monthly EMA(Monthly Close, 89)
        cond3 = current['HA_Open'] <= current['EMA_89_Close']
        criteria_results.append(f"HA_Open({current['HA_Open']:.2f}) <= EMA89({current['EMA_89_Close']:.2f}): {cond3}")
        
        # Condition 4: 89 months ago Close > 0
        cond4 = eighty_nine_months_ago['Close'] > 0
        criteria_results.append(f"89mo ago Close({eighty_nine_months_ago['Close']:.2f}) > 0: {cond4}")
        
        # Condition 5: 1 month ago HA-Close < Monthly EMA(Monthly Close, 89)
        cond5 = one_month_ago['HA_Close'] < one_month_ago['EMA_89_Close']
        criteria_results.append(f"1mo ago HA_Close({one_month_ago['HA_Close']:.2f}) < EMA89({one_month_ago['EMA_89_Close']:.2f}): {cond5}")
        
        # All conditions must be true
        all_conditions_met = cond1 and cond2 and cond3 and cond4 and cond5
        
        return all_conditions_met, criteria_results
    
    def analyze_stock(self, symbol, market_cap):
        """Analyze a single stock for refined signals"""
        print(f"Analyzing {symbol} ({market_cap}) with refined criteria...")
        
        data = self.fetch_stock_data(symbol)
        if data is None or len(data) < 91:  # Need at least 89 periods + 1 month ago + current
            print(f"  Skipping {symbol} - insufficient data")
            return
        
        signals_found = 0
        
        # Check each month from index 90 onwards (need 89 months of history + 1 month ago)
        for i in range(90, len(data)):
            conditions_met, details = self.check_refined_criteria(data, i)
            
            if conditions_met:
                signals_found += 1
                current = data.iloc[i]
                
                print(f"  SIGNAL FOUND at {data.index[i].strftime('%Y-%m-%d')}")
                for detail in details:
                    print(f"    {detail}")
                
                self.results.append({
                    'Date': data.index[i].strftime('%Y-%m-%d'),
                    'Stock_Ticker': symbol.replace('.NS', ''),
                    'Market_Cap': market_cap,
                    'HA_Close': round(current['HA_Close'], 2),
                    'HA_Open': round(current['HA_Open'], 2),
                    'EMA_89_Close': round(current['EMA_89_Close'], 2),
                    'Regular_Close': round(current['Close'], 2)
                })
        
        if signals_found == 0:
            print(f"  No refined signals found for {symbol}")
        else:
            print(f"  Found {signals_found} refined signals for {symbol}")
        
        time.sleep(1)  # Rate limiting
    
    def run_analysis(self):
        """Run the refined analysis"""
        print("REFINED Nifty 500 Analysis with Advanced Criteria")
        print("=" * 70)
        print("Refined Conditions:")
        print("1. Monthly HA-Close > Monthly HA-Open")
        print("2. Monthly HA-Close > Monthly EMA(Monthly Close, 89)")
        print("3. Monthly HA-Open <= Monthly EMA(Monthly Close, 89)")
        print("4. 89 months ago Close > 0")
        print("5. 1 month ago HA-Close < Monthly EMA(Monthly Close, 89)")
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
            
            print(f"\nREFINED ANALYSIS COMPLETE!")
            print(f"Found {len(results_df)} REFINED signals (vs 3,830 basic signals)")
            print("=" * 70)
            print("Recent Refined Signals:")
            print("=" * 70)
            print(results_df[['Date', 'Stock_Ticker', 'Market_Cap']].head(20).to_string(index=False))
            
            # Save to CSV
            results_df.to_csv('refined_nifty500_signals.csv', index=False)
            print(f"\nRefined results saved to 'refined_nifty500_signals.csv'")
            
            # Summary by market cap
            print("\nSummary by Market Cap:")
            print("=" * 30)
            summary = results_df.groupby('Market_Cap').size().reset_index(name='Refined_Signal_Count')
            print(summary.to_string(index=False))
            
            # Show sample of detailed results
            print("\nSample Detailed Results:")
            print("=" * 80)
            sample_detailed = results_df.head(10)[['Date', 'Stock_Ticker', 'Market_Cap', 'HA_Close', 'HA_Open', 'EMA_89_Close']]
            print(sample_detailed.to_string(index=False))
            
        else:
            print("No refined signals found matching all criteria.")
        
        return results_df

if __name__ == "__main__":
    analyzer = RefinedStockAnalyzer()
    results = analyzer.run_analysis()
