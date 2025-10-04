import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import time

class BacktestingFramework:
    def __init__(self):
        self.trades = []
        self.performance_metrics = {}
        
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
        
        # Calculate Heikin Ashi body and shadows for doji detection
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
    
    def fetch_trading_data(self, symbol, signal_date, months_after=24):
        """Fetch data for backtesting from signal date onwards"""
        try:
            signal_dt = datetime.strptime(signal_date, '%Y-%m-%d')
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
            print(f"  Error fetching trading data for {symbol}: {e}")
            return None
    
    def find_entry_point(self, data, signal_high):
        """Find entry point: candle that cuts high of signal candle and is above 21 EMA"""
        for i in range(len(data)):
            current = data.iloc[i]
            
            # Check if current candle cuts the signal high and is above 21 EMA
            if (current['High'] > signal_high and 
                current['Close'] > current['EMA_21'] and
                not pd.isna(current['EMA_21'])):
                
                return i, current['Close']  # Entry at close of the candle
        
        return None, None
    
    def find_stop_loss(self, data, entry_idx):
        """Find stop loss: monthly candle closes below 21 EMA"""
        for i in range(entry_idx + 1, len(data)):
            current = data.iloc[i]
            
            if current['Close'] < current['EMA_21']:
                return i, current['Close'], 'Stop Loss'
        
        return None, None, None
    
    def find_target_1(self, data, entry_idx):
        """Find Target 1: first red long-legged doji Heikin Ashi"""
        for i in range(entry_idx + 1, len(data)):
            current = data.iloc[i]
            
            if current['Is_Red_Doji']:
                return i, current['Close'], 'Target 1 - Red Doji'
        
        return None, None, None
    
    def find_target_2(self, data, entry_idx, entry_price):
        """Find Target 2: candle closes below 21 EMA from recent high"""
        highest_price = entry_price
        highest_idx = entry_idx
        
        # Track the highest price after entry
        for i in range(entry_idx + 1, len(data)):
            current = data.iloc[i]
            
            if current['High'] > highest_price:
                highest_price = current['High']
                highest_idx = i
            
            # Check if current candle closes below 21 EMA
            if current['Close'] < current['EMA_21']:
                return i, current['Close'], 'Target 2 - Below 21 EMA'
        
        return None, None, None
    
    def backtest_signal(self, symbol, signal_date, signal_high):
        """Backtest a single signal"""
        print(f"  Backtesting {symbol} - {signal_date}")
        
        # Fetch trading data
        data = self.fetch_trading_data(symbol, signal_date)
        if data is None:
            return None
        
        # Find entry point
        entry_idx, entry_price = self.find_entry_point(data, signal_high)
        if entry_idx is None:
            return {
                'symbol': symbol,
                'signal_date': signal_date,
                'status': 'No Entry Found',
                'entry_price': None,
                'exit_price': None,
                'exit_date': None,
                'exit_reason': 'No Entry',
                'return_percent': 0,
                'months_held': 0
            }
        
        entry_date = data.index[entry_idx].strftime('%Y-%m-%d')
        
        # Find exit points (whichever comes first)
        stop_idx, stop_price, stop_reason = self.find_stop_loss(data, entry_idx)
        target1_idx, target1_price, target1_reason = self.find_target_1(data, entry_idx)
        target2_idx, target2_price, target2_reason = self.find_target_2(data, entry_idx, entry_price)
        
        # Determine which exit occurs first
        exits = []
        if stop_idx is not None:
            exits.append((stop_idx, stop_price, stop_reason))
        if target1_idx is not None:
            exits.append((target1_idx, target1_price, target1_reason))
        if target2_idx is not None:
            exits.append((target2_idx, target2_price, target2_reason))
        
        if not exits:
            # No exit found, use last available data
            last_idx = len(data) - 1
            exit_price = data.iloc[last_idx]['Close']
            exit_reason = 'End of Data'
            exit_date = data.index[last_idx].strftime('%Y-%m-%d')
            months_held = last_idx - entry_idx
        else:
            # Use the earliest exit
            exit_idx, exit_price, exit_reason = min(exits, key=lambda x: x[0])
            exit_date = data.index[exit_idx].strftime('%Y-%m-%d')
            months_held = exit_idx - entry_idx
        
        # Calculate return
        return_percent = ((exit_price - entry_price) / entry_price) * 100
        
        return {
            'symbol': symbol,
            'signal_date': signal_date,
            'status': 'Completed',
            'entry_price': round(entry_price, 2),
            'entry_date': entry_date,
            'exit_price': round(exit_price, 2),
            'exit_date': exit_date,
            'exit_reason': exit_reason,
            'return_percent': round(return_percent, 2),
            'months_held': months_held,
            'signal_high': signal_high
        }
    
    def run_backtest(self, signals_file='full_nifty500_signals.csv'):
        """Run backtest on all signals"""
        print("=== BACKTESTING FRAMEWORK ===")
        print("Entry: Cut high of signal candle + above 21 EMA")
        print("Stop Loss: Monthly candle closes below 21 EMA")
        print("Target 1: First red long-legged doji Heikin Ashi")
        print("Target 2: Candle closes below 21 EMA from recent high")
        print("=" * 60)
        
        # Load signals
        try:
            signals_df = pd.read_csv(signals_file)
        except FileNotFoundError:
            print(f"Signals file {signals_file} not found. Please run full analysis first.")
            return None
        
        print(f"Backtesting {len(signals_df)} signals...")
        
        # Backtest each signal
        for idx, signal in signals_df.iterrows():
            result = self.backtest_signal(
                signal['Stock_Ticker'], 
                signal['Date'], 
                signal['Signal_High']
            )
            
            if result:
                self.trades.append(result)
            
            # Progress indicator
            if (idx + 1) % 10 == 0:
                print(f"  Processed {idx + 1}/{len(signals_df)} signals...")
            
            time.sleep(0.1)  # Rate limiting
        
        # Convert results to DataFrame
        results_df = pd.DataFrame(self.trades)
        
        if not results_df.empty:
            # Save results
            results_df.to_csv('backtest_results.csv', index=False)
            print(f"\nBacktest results saved to 'backtest_results.csv'")
            
            # Generate performance analysis
            self.analyze_performance(results_df)
        
        return results_df
    
    def analyze_performance(self, results_df):
        """Analyze backtesting performance"""
        print("\n=== PERFORMANCE ANALYSIS ===")
        
        # Basic statistics
        total_trades = len(results_df)
        completed_trades = len(results_df[results_df['status'] == 'Completed'])
        
        print(f"Total Signals: {total_trades}")
        print(f"Completed Trades: {completed_trades}")
        print(f"Entry Success Rate: {(completed_trades/total_trades)*100:.1f}%")
        
        if completed_trades > 0:
            # Return analysis
            returns = results_df[results_df['status'] == 'Completed']['return_percent']
            
            print(f"\nReturn Statistics:")
            print(f"  Average Return: {returns.mean():.2f}%")
            print(f"  Median Return: {returns.median():.2f}%")
            print(f"  Best Return: {returns.max():.2f}%")
            print(f"  Worst Return: {returns.min():.2f}%")
            print(f"  Standard Deviation: {returns.std():.2f}%")
            
            # Win/Loss analysis
            winning_trades = len(returns[returns > 0])
            losing_trades = len(returns[returns <= 0])
            
            print(f"\nWin/Loss Analysis:")
            print(f"  Winning Trades: {winning_trades} ({(winning_trades/completed_trades)*100:.1f}%)")
            print(f"  Losing Trades: {losing_trades} ({(losing_trades/completed_trades)*100:.1f}%)")
            
            # Exit reason analysis
            print(f"\nExit Reason Analysis:")
            exit_reasons = results_df[results_df['status'] == 'Completed']['exit_reason'].value_counts()
            for reason, count in exit_reasons.items():
                print(f"  {reason}: {count} trades ({(count/completed_trades)*100:.1f}%)")
            
            # Time analysis
            months_held = results_df[results_df['status'] == 'Completed']['months_held']
            print(f"\nTime Analysis:")
            print(f"  Average Months Held: {months_held.mean():.1f}")
            print(f"  Median Months Held: {months_held.median():.1f}")
            print(f"  Max Months Held: {months_held.max()}")
            
            # Risk metrics
            sharpe_ratio = returns.mean() / returns.std() if returns.std() > 0 else 0
            max_drawdown = returns.min()
            
            print(f"\nRisk Metrics:")
            print(f"  Sharpe Ratio: {sharpe_ratio:.2f}")
            print(f"  Maximum Drawdown: {max_drawdown:.2f}%")
            
            # Save detailed analysis
            performance_summary = {
                'total_signals': total_trades,
                'completed_trades': completed_trades,
                'entry_success_rate': (completed_trades/total_trades)*100,
                'average_return': returns.mean(),
                'win_rate': (winning_trades/completed_trades)*100,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown
            }
            
            pd.DataFrame([performance_summary]).to_csv('performance_summary.csv', index=False)
            print(f"\nPerformance summary saved to 'performance_summary.csv'")

if __name__ == "__main__":
    backtester = BacktestingFramework()
    results = backtester.run_backtest()


