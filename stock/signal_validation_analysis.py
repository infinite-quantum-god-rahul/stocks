import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

class SignalValidationAnalyzer:
    def __init__(self):
        self.validation_results = []
        
    def calculate_heikin_ashi(self, df):
        """Calculate Heikin Ashi candlesticks"""
        ha_df = df.copy()
        ha_df['HA_Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
        ha_df['HA_Open'] = 0.0
        ha_df.iloc[0, ha_df.columns.get_loc('HA_Open')] = df.iloc[0]['Open']
        
        for i in range(1, len(ha_df)):
            ha_df.iloc[i, ha_df.columns.get_loc('HA_Open')] = (ha_df.iloc[i-1]['HA_Open'] + ha_df.iloc[i-1]['HA_Close']) / 2
        
        ha_df['HA_High'] = ha_df[['High', 'HA_Open', 'HA_Close']].max(axis=1)
        ha_df['HA_Low'] = ha_df[['Low', 'HA_Open', 'HA_Close']].min(axis=1)
        return ha_df
    
    def calculate_ema(self, prices, period):
        """Calculate Exponential Moving Average"""
        return prices.ewm(span=period).mean()
    
    def find_actual_crossover(self, symbol, signal_date):
        """Find the actual first crossover date from chart analysis"""
        # Fetch extended data to find the true crossover
        end_date = datetime.now()
        start_date = end_date - timedelta(days=15 * 365)
        
        ticker = yf.Ticker(symbol)
        data = ticker.history(start=start_date, end=end_date, interval='1mo')
        
        if data.empty:
            return None, None
        
        data = self.calculate_heikin_ashi(data)
        data['EMA_89_HA'] = self.calculate_ema(data['HA_Close'], 89)
        
        # Find the first crossover (HA_Close crossing above EMA)
        first_crossover = None
        crossover_details = None
        
        for i in range(90, len(data)):  # Start after EMA is available
            current = data.iloc[i]
            previous = data.iloc[i-1]
            
            # Check if this is a crossover from below to above
            if (previous['HA_Close'] <= previous['EMA_89_HA'] and 
                current['HA_Close'] > current['EMA_89_HA']):
                first_crossover = data.index[i]
                crossover_details = {
                    'date': first_crossover,
                    'ha_close': current['HA_Close'],
                    'ema': current['EMA_89_HA'],
                    'prev_ha_close': previous['HA_Close'],
                    'prev_ema': previous['EMA_89_HA']
                }
                break
        
        return first_crossover, crossover_details
    
    def validate_signal(self, signal_date, stock_ticker):
        """Validate a signal against actual crossover"""
        actual_crossover, details = self.find_actual_crossover(stock_ticker, signal_date)
        
        if actual_crossover is None:
            return {
                'stock': stock_ticker,
                'signal_date': signal_date,
                'actual_crossover': None,
                'months_diff': None,
                'validity': 'NO_CROSSOVER_FOUND',
                'details': 'No clear crossover found in data'
            }
        
        # Calculate difference in months
        signal_dt = pd.to_datetime(signal_date)
        actual_dt = pd.to_datetime(actual_crossover)
        
        months_diff = (signal_dt.year - actual_dt.year) * 12 + (signal_dt.month - actual_dt.month)
        
        # Determine validity
        if abs(months_diff) <= 1:
            validity = 'EXCELLENT'
        elif abs(months_diff) <= 2:
            validity = 'GOOD'
        elif abs(months_diff) <= 3:
            validity = 'ACCEPTABLE'
        elif abs(months_diff) <= 4:
            validity = 'POOR'
        else:
            validity = 'INVALID'
        
        return {
            'stock': stock_ticker,
            'signal_date': signal_date,
            'actual_crossover': actual_crossover.strftime('%Y-%m-%d'),
            'months_diff': months_diff,
            'validity': validity,
            'details': details
        }
    
    def analyze_all_signals(self):
        """Analyze all signals from our results"""
        # Read our corrected results
        results_df = pd.read_csv('corrected_nifty500_signals.csv')
        
        print("=== SIGNAL VALIDATION ANALYSIS ===")
        print(f"Total signals to validate: {len(results_df)}")
        print("=" * 60)
        
        for idx, row in results_df.iterrows():
            print(f"Validating {row['Stock_Ticker']} - {row['Date']}...")
            
            validation = self.validate_signal(row['Date'], row['Stock_Ticker'])
            self.validation_results.append(validation)
            
            print(f"  Actual crossover: {validation['actual_crossover']}")
            print(f"  Difference: {validation['months_diff']} months")
            print(f"  Validity: {validation['validity']}")
            print("-" * 40)
            
            time.sleep(0.5)  # Rate limiting
    
    def generate_summary(self):
        """Generate validation summary"""
        if not self.validation_results:
            print("No validation results available")
            return
        
        # Convert to DataFrame for analysis
        validation_df = pd.DataFrame(self.validation_results)
        
        print("\n=== VALIDATION SUMMARY ===")
        print("=" * 50)
        
        # Count by validity
        validity_counts = validation_df['validity'].value_counts()
        print("Validity Distribution:")
        for validity, count in validity_counts.items():
            percentage = (count / len(validation_df)) * 100
            print(f"  {validity}: {count} signals ({percentage:.1f}%)")
        
        # Analyze months difference
        valid_months = validation_df[validation_df['months_diff'].notna()]['months_diff']
        if len(valid_months) > 0:
            print(f"\nMonths Difference Statistics:")
            print(f"  Mean: {valid_months.mean():.1f} months")
            print(f"  Median: {valid_months.median():.1f} months")
            print(f"  Std Dev: {valid_months.std():.1f} months")
            print(f"  Range: {valid_months.min()} to {valid_months.max()} months")
        
        # Show problematic signals
        print(f"\n=== PROBLEMATIC SIGNALS (Difference > 3 months) ===")
        problematic = validation_df[validation_df['months_diff'].abs() > 3]
        if len(problematic) > 0:
            for _, row in problematic.iterrows():
                print(f"  {row['stock']} - Signal: {row['signal_date']}, Actual: {row['actual_crossover']}, Diff: {row['months_diff']} months")
        else:
            print("  No problematic signals found!")
        
        # Show excellent signals
        print(f"\n=== EXCELLENT SIGNALS (Difference ≤ 1 month) ===")
        excellent = validation_df[validation_df['validity'] == 'EXCELLENT']
        if len(excellent) > 0:
            for _, row in excellent.iterrows():
                print(f"  {row['stock']} - Signal: {row['signal_date']}, Actual: {row['actual_crossover']}, Diff: {row['months_diff']} months")
        
        # Save detailed results
        validation_df.to_csv('signal_validation_results.csv', index=False)
        print(f"\nDetailed validation results saved to 'signal_validation_results.csv'")
        
        return validation_df

def main():
    analyzer = SignalValidationAnalyzer()
    analyzer.analyze_all_signals()
    analyzer.generate_summary()

if __name__ == "__main__":
    main()


