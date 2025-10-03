import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import warnings
import gc
warnings.filterwarnings('ignore')

class FullPositionAnalyzer:
    def __init__(self):
        self.results = []
        
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
    
    def analyze_position(self, signal_row):
        """Analyze a single position comprehensively"""
        symbol = signal_row['symbol']
        signal_date = signal_row['date']
        market_cap = signal_row['marketcapname']
        sector = signal_row['sector']
        
        # Fetch trading data
        data = self.fetch_stock_data(symbol, signal_date)
        if data is None:
            return {
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
    
    def run_full_analysis(self, signals_file):
        """Run comprehensive analysis on all signals"""
        print("=== FULL POSITION ANALYSIS ===")
        print("Analyzing ALL 2,847 signals for Entry, Exit, Targets, CAGR, Max High, Drawdown")
        print("=" * 60)
        
        # Load signals
        try:
            signals_df = pd.read_csv(signals_file)
        except FileNotFoundError:
            print(f"Signals file {signals_file} not found.")
            return None
        
        print(f"Analyzing ALL {len(signals_df)} signals...")
        
        # Process in batches to manage memory
        batch_size = 100
        total_batches = (len(signals_df) + batch_size - 1) // batch_size
        
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min((batch_num + 1) * batch_size, len(signals_df))
            batch_df = signals_df.iloc[start_idx:end_idx]
            
            print(f"\nProcessing Batch {batch_num + 1}/{total_batches} (Signals {start_idx + 1}-{end_idx})")
            
            # Analyze each signal in the batch
            for idx, signal in batch_df.iterrows():
                result = self.analyze_position(signal)
                self.results.append(result)
                
                # Progress indicator
                if (idx - start_idx + 1) % 10 == 0:
                    print(f"  Processed {idx - start_idx + 1}/{len(batch_df)} signals in batch...")
                
                time.sleep(0.05)  # Rate limiting
            
            # Save intermediate results after each batch
            if self.results:
                temp_df = pd.DataFrame(self.results)
                temp_df.to_csv(f'position_analysis_batch_{batch_num + 1}.csv', index=False)
                print(f"  Batch {batch_num + 1} results saved: {len(batch_df)} signals processed")
            
            # Clear memory between batches
            gc.collect()
        
        # Convert all results to DataFrame
        results_df = pd.DataFrame(self.results)
        
        if not results_df.empty:
            # Save final results
            results_df.to_csv('full_position_analysis.csv', index=False)
            print(f"\n=== FULL ANALYSIS COMPLETE ===")
            print(f"Total signals analyzed: {len(results_df)}")
            print(f"Final results saved to 'full_position_analysis.csv'")
            
            # Generate summary statistics
            self.generate_summary_stats(results_df)
        
        return results_df
    
    def generate_summary_stats(self, results_df):
        """Generate summary statistics"""
        print("\n=== SUMMARY STATISTICS ===")
        
        completed_trades = results_df[results_df['status'] == 'Completed']
        print(f"Total Signals: {len(results_df)}")
        print(f"Completed Trades: {len(completed_trades)}")
        print(f"Success Rate: {(len(completed_trades)/len(results_df))*100:.1f}%")
        
        if len(completed_trades) > 0:
            returns = completed_trades['total_return_percent']
            print(f"\nReturn Statistics:")
            print(f"  Average Return: {returns.mean():.2f}%")
            print(f"  Median Return: {returns.median():.2f}%")
            print(f"  Best Return: {returns.max():.2f}%")
            print(f"  Worst Return: {returns.min():.2f}%")
            
            print(f"\nCAGR Statistics:")
            cagr_values = completed_trades['cagr_percent']
            print(f"  Average CAGR: {cagr_values.mean():.2f}%")
            print(f"  Median CAGR: {cagr_values.median():.2f}%")
            
            print(f"\nDrawdown Statistics:")
            drawdown_values = completed_trades['drawdown_percent']
            print(f"  Average Drawdown: {drawdown_values.mean():.2f}%")
            print(f"  Max Drawdown: {drawdown_values.max():.2f}%")
            
            print(f"\nExit Reason Analysis:")
            exit_reasons = completed_trades['exit_reason'].value_counts()
            for reason, count in exit_reasons.items():
                print(f"  {reason}: {count} trades ({(count/len(completed_trades))*100:.1f}%)")

if __name__ == "__main__":
    analyzer = FullPositionAnalyzer()
    results = analyzer.run_full_analysis('Backtest Monthly HA and MACD')
