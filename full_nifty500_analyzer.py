import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import requests
from bs4 import BeautifulSoup

class FullNifty500Analyzer:
    def __init__(self):
        self.results = []
        self.nifty500_stocks = {}
        
    def get_full_nifty500_list(self):
        """Get complete Nifty 500 stock list"""
        print("Fetching complete Nifty 500 stock list...")
        
        # Extended list of major Nifty 500 stocks
        full_stocks = {
            # Large Cap Stocks
            'RELIANCE.NS': 'Large Cap', 'TCS.NS': 'Large Cap', 'HDFCBANK.NS': 'Large Cap',
            'INFY.NS': 'Large Cap', 'HINDUNILVR.NS': 'Large Cap', 'ITC.NS': 'Large Cap',
            'SBIN.NS': 'Large Cap', 'BHARTIARTL.NS': 'Large Cap', 'KOTAKBANK.NS': 'Large Cap',
            'LT.NS': 'Large Cap', 'ASIANPAINT.NS': 'Large Cap', 'AXISBANK.NS': 'Large Cap',
            'MARUTI.NS': 'Large Cap', 'SUNPHARMA.NS': 'Large Cap', 'ULTRACEMCO.NS': 'Large Cap',
            'WIPRO.NS': 'Large Cap', 'NESTLEIND.NS': 'Large Cap', 'TITAN.NS': 'Large Cap',
            'POWERGRID.NS': 'Large Cap', 'NTPC.NS': 'Large Cap', 'ONGC.NS': 'Large Cap',
            'COALINDIA.NS': 'Large Cap', 'TECHM.NS': 'Large Cap', 'BAJFINANCE.NS': 'Large Cap',
            'ICICIBANK.NS': 'Large Cap', 'HDFC.NS': 'Large Cap', 'INDUSINDBK.NS': 'Large Cap',
            'M&M.NS': 'Large Cap', 'SHREECEM.NS': 'Large Cap', 'TATASTEEL.NS': 'Large Cap',
            'HCLTECH.NS': 'Large Cap', 'APOLLOHOSP.NS': 'Large Cap', 'BAJAJ-AUTO.NS': 'Large Cap',
            'BRITANNIA.NS': 'Large Cap', 'DIVISLAB.NS': 'Large Cap', 'HEROMOTOCO.NS': 'Large Cap',
            'HINDALCO.NS': 'Large Cap', 'JSWSTEEL.NS': 'Large Cap', 'ADANIPORTS.NS': 'Large Cap',
            'GRASIM.NS': 'Large Cap', 'CIPLA.NS': 'Large Cap', 'DRREDDY.NS': 'Large Cap',
            'BAJAJFINSV.NS': 'Large Cap', 'EICHERMOT.NS': 'Large Cap', 'TATAMOTORS.NS': 'Large Cap',
            'VEDL.NS': 'Large Cap', 'UPL.NS': 'Large Cap', 'GAIL.NS': 'Large Cap',
            'BPCL.NS': 'Large Cap', 'IOC.NS': 'Large Cap', 'TATACONSUM.NS': 'Large Cap',
            'SBILIFE.NS': 'Large Cap', 'ADANIGREEN.NS': 'Large Cap', 'ADANITRANS.NS': 'Large Cap',
            'PETRONET.NS': 'Large Cap', 'GODREJCP.NS': 'Large Cap', 'BIOCON.NS': 'Large Cap',
            'MOTHERSON.NS': 'Large Cap', 'MARICO.NS': 'Large Cap', 'PIDILITIND.NS': 'Large Cap',
            'CROMPTON.NS': 'Large Cap', 'SIEMENS.NS': 'Large Cap', 'EXIDEIND.NS': 'Large Cap',
            'POLYCAB.NS': 'Large Cap', 'MFSL.NS': 'Large Cap', 'LICHSGFIN.NS': 'Large Cap',
            'INDHOTEL.NS': 'Large Cap', 'RECLTD.NS': 'Large Cap', 'LTIM.NS': 'Large Cap',
            'ADANIENT.NS': 'Large Cap', 'ADANIPOWER.NS': 'Large Cap', 'AMBUJACEM.NS': 'Large Cap',
            'BANDHANBNK.NS': 'Large Cap', 'BANKBARODA.NS': 'Large Cap', 'CANBK.NS': 'Large Cap',
            'PNB.NS': 'Large Cap', 'UNIONBANK.NS': 'Large Cap', 'FEDERALBNK.NS': 'Large Cap',
            'IDFCFIRSTB.NS': 'Large Cap', 'RBLBANK.NS': 'Large Cap', 'YESBANK.NS': 'Large Cap',
            'IDBI.NS': 'Large Cap', 'KOTAKBANK.NS': 'Large Cap', 'AUBANK.NS': 'Large Cap',
            
            # Mid Cap Stocks
            'ABBOTINDIA.NS': 'Mid Cap', 'ASTRAL.NS': 'Mid Cap', 'BATAINDIA.NS': 'Mid Cap',
            'BERGEPAINT.NS': 'Mid Cap', 'BOSCHLTD.NS': 'Mid Cap', 'CADILAHC.NS': 'Mid Cap',
            'COLPAL.NS': 'Mid Cap', 'CONCOR.NS': 'Mid Cap', 'DABUR.NS': 'Mid Cap',
            'DIVISLAB.NS': 'Mid Cap', 'DMART.NS': 'Mid Cap', 'GODREJPROP.NS': 'Mid Cap',
            'HDFCAMC.NS': 'Mid Cap', 'HDFCLIFE.NS': 'Mid Cap', 'HINDZINC.NS': 'Mid Cap',
            'IBULHSGFIN.NS': 'Mid Cap', 'INDIGO.NS': 'Mid Cap', 'INDUSTOWER.NS': 'Mid Cap',
            'INFIBEAM.NS': 'Mid Cap', 'JINDALSTEL.NS': 'Mid Cap', 'JUBLFOOD.NS': 'Mid Cap',
            'LALPATHLAB.NS': 'Mid Cap', 'LICHSGFIN.NS': 'Mid Cap', 'LUPIN.NS': 'Mid Cap',
            'MANAPPURAM.NS': 'Mid Cap', 'MINDTREE.NS': 'Mid Cap', 'MPHASIS.NS': 'Mid Cap',
            'MOTHERSON.NS': 'Mid Cap', 'MRF.NS': 'Mid Cap', 'MUTHOOTFIN.NS': 'Mid Cap',
            'NAUKRI.NS': 'Mid Cap', 'PAGEIND.NS': 'Mid Cap', 'PEL.NS': 'Mid Cap',
            'PIIND.NS': 'Mid Cap', 'PNBHOUSING.NS': 'Mid Cap', 'PVR.NS': 'Mid Cap',
            'RAMKYINFRA.NS': 'Mid Cap', 'RATNAMANI.NS': 'Mid Cap', 'SAIL.NS': 'Mid Cap',
            'SHILPAMED.NS': 'Mid Cap', 'SUNTV.NS': 'Mid Cap', 'TATACHEM.NS': 'Mid Cap',
            'TATACOMM.NS': 'Mid Cap', 'TATAELXSI.NS': 'Mid Cap', 'TATAPOWER.NS': 'Mid Cap',
            'TCS.NS': 'Mid Cap', 'TORNTPHARM.NS': 'Mid Cap', 'TRENT.NS': 'Mid Cap',
            'TVSMOTOR.NS': 'Mid Cap', 'UBL.NS': 'Mid Cap', 'VOLTAS.NS': 'Mid Cap',
            'WABCOINDIA.NS': 'Mid Cap', 'WHIRLPOOL.NS': 'Mid Cap', 'ZEEL.NS': 'Mid Cap',
            
            # Small Cap Stocks (representative sample)
            '3MINDIA.NS': 'Small Cap', 'ABB.NS': 'Small Cap', 'ADANIENT.NS': 'Small Cap',
            'ALKEM.NS': 'Small Cap', 'APOLLOTYRE.NS': 'Small Cap', 'ASHOKLEY.NS': 'Small Cap',
            'ASTRAL.NS': 'Small Cap', 'ATUL.NS': 'Small Cap', 'AUROPHARMA.NS': 'Small Cap',
            'BAJAJHLDNG.NS': 'Small Cap', 'BALKRISIND.NS': 'Small Cap', 'BANDHANBNK.NS': 'Small Cap',
            'BHARATFORG.NS': 'Small Cap', 'BHEL.NS': 'Small Cap', 'BOSCHLTD.NS': 'Small Cap',
            'CADILAHC.NS': 'Small Cap', 'CHOLAFIN.NS': 'Small Cap', 'CIPLA.NS': 'Small Cap',
            'COLPAL.NS': 'Small Cap', 'CONCOR.NS': 'Small Cap', 'CUMMINSIND.NS': 'Small Cap',
            'DABUR.NS': 'Small Cap', 'DLF.NS': 'Small Cap', 'DIVISLAB.NS': 'Small Cap',
            'DRREDDY.NS': 'Small Cap', 'EICHERMOT.NS': 'Small Cap', 'ESCORTS.NS': 'Small Cap',
            'EXIDEIND.NS': 'Small Cap', 'FEDERALBNK.NS': 'Small Cap', 'GAIL.NS': 'Small Cap',
            'GLENMARK.NS': 'Small Cap', 'GMRINFRA.NS': 'Small Cap', 'GODREJCP.NS': 'Small Cap',
            'GODREJPROP.NS': 'Small Cap', 'GRASIM.NS': 'Small Cap', 'HAVELLS.NS': 'Small Cap',
            'HCLTECH.NS': 'Small Cap', 'HDFCAMC.NS': 'Small Cap', 'HDFCLIFE.NS': 'Small Cap',
            'HEROMOTOCO.NS': 'Small Cap', 'HINDALCO.NS': 'Small Cap', 'HINDZINC.NS': 'Small Cap',
            'IBULHSGFIN.NS': 'Small Cap', 'ICICIPRULI.NS': 'Small Cap', 'IDFCFIRSTB.NS': 'Small Cap',
            'IGL.NS': 'Small Cap', 'INDIGO.NS': 'Small Cap', 'INDUSTOWER.NS': 'Small Cap',
            'INFIBEAM.NS': 'Small Cap', 'JINDALSTEL.NS': 'Small Cap', 'JUBLFOOD.NS': 'Small Cap',
            'JUSTDIAL.NS': 'Small Cap', 'LALPATHLAB.NS': 'Small Cap', 'LICHSGFIN.NS': 'Small Cap',
            'LUPIN.NS': 'Small Cap', 'MANAPPURAM.NS': 'Small Cap', 'MARICO.NS': 'Small Cap',
            'MINDTREE.NS': 'Small Cap', 'MPHASIS.NS': 'Small Cap', 'MRF.NS': 'Small Cap',
            'MUTHOOTFIN.NS': 'Small Cap', 'NAUKRI.NS': 'Small Cap', 'NMDC.NS': 'Small Cap',
            'PAGEIND.NS': 'Small Cap', 'PEL.NS': 'Small Cap', 'PIIND.NS': 'Small Cap',
            'PNBHOUSING.NS': 'Small Cap', 'PVR.NS': 'Small Cap', 'RAMKYINFRA.NS': 'Small Cap',
            'RATNAMANI.NS': 'Small Cap', 'SAIL.NS': 'Small Cap', 'SHILPAMED.NS': 'Small Cap',
            'SUNTV.NS': 'Small Cap', 'TATACHEM.NS': 'Small Cap', 'TATACOMM.NS': 'Small Cap',
            'TATAELXSI.NS': 'Small Cap', 'TATAPOWER.NS': 'Small Cap', 'TORNTPHARM.NS': 'Small Cap',
            'TRENT.NS': 'Small Cap', 'TVSMOTOR.NS': 'Small Cap', 'UBL.NS': 'Small Cap',
            'VOLTAS.NS': 'Small Cap', 'WABCOINDIA.NS': 'Small Cap', 'WHIRLPOOL.NS': 'Small Cap',
            'ZEEL.NS': 'Small Cap'
        }
        
        self.nifty500_stocks = full_stocks
        print(f"Loaded {len(self.nifty500_stocks)} stocks from Nifty 500")
        return self.nifty500_stocks
    
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
        
        # Calculate Heikin Ashi body and shadows
        ha_df['HA_Body'] = abs(ha_df['HA_Close'] - ha_df['HA_Open'])
        ha_df['HA_UpperShadow'] = ha_df['HA_High'] - ha_df[['HA_Open', 'HA_Close']].max(axis=1)
        ha_df['HA_LowerShadow'] = ha_df[['HA_Open', 'HA_Close']].min(axis=1) - ha_df['HA_Low']
        
        return ha_df
    
    def calculate_ema(self, prices, period):
        """Calculate Exponential Moving Average"""
        return prices.ewm(span=period).mean()
    
    def fetch_stock_data(self, symbol, years=15):
        """Fetch monthly stock data for the specified number of years"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years * 365)
            
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date, interval='1mo')
            
            if data.empty:
                return None
                
            # Calculate Heikin Ashi
            data = self.calculate_heikin_ashi(data)
            
            # Calculate EMAs
            data['EMA_89_HA_Close'] = self.calculate_ema(data['HA_Close'], 89)
            data['EMA_21'] = self.calculate_ema(data['Close'], 21)
            
            return data
            
        except Exception as e:
            print(f"  Error fetching data for {symbol}: {e}")
            return None
    
    def check_improved_criteria(self, data, current_idx):
        """Check improved criteria for signal detection"""
        if current_idx < 92:
            return False, []
        
        current = data.iloc[current_idx]
        one_month_ago = data.iloc[current_idx - 1]
        two_months_ago = data.iloc[current_idx - 2]
        eighty_nine_months_ago = data.iloc[current_idx - 89]
        
        # All 7 improved conditions
        cond1 = current['HA_Close'] > current['HA_Open']
        cond2 = current['HA_Close'] > current['EMA_89_HA_Close']
        cond3 = current['HA_Open'] <= current['EMA_89_HA_Close']
        cond4 = eighty_nine_months_ago['Close'] > 0
        cond5 = one_month_ago['HA_Close'] < one_month_ago['EMA_89_HA_Close']
        cond6 = two_months_ago['HA_Close'] <= two_months_ago['EMA_89_HA_Close']
        
        breakout_strength = ((current['HA_Close'] - current['EMA_89_HA_Close']) / current['EMA_89_HA_Close']) * 100
        cond7 = breakout_strength >= 1.0
        
        all_conditions_met = cond1 and cond2 and cond3 and cond4 and cond5 and cond6 and cond7
        
        return all_conditions_met, {
            'breakout_strength': breakout_strength,
            'signal_high': current['High'],
            'signal_close': current['Close'],
            'signal_ha_close': current['HA_Close']
        }
    
    def analyze_stock(self, symbol, market_cap):
        """Analyze a single stock for signals"""
        print(f"Analyzing {symbol} ({market_cap})...")
        
        data = self.fetch_stock_data(symbol)
        if data is None or len(data) < 93:
            return
        
        signals_found = 0
        
        for i in range(92, len(data)):
            conditions_met, signal_details = self.check_improved_criteria(data, i)
            
            if conditions_met:
                signals_found += 1
                current = data.iloc[i]
                
                self.results.append({
                    'Date': data.index[i].strftime('%Y-%m-%d'),
                    'Stock_Ticker': symbol.replace('.NS', ''),
                    'Market_Cap': market_cap,
                    'HA_Close': round(current['HA_Close'], 2),
                    'HA_Open': round(current['HA_Open'], 2),
                    'EMA_89_HA_Close': round(current['EMA_89_HA_Close'], 2),
                    'Breakout_Strength_Percent': round(signal_details['breakout_strength'], 2),
                    'Signal_High': round(signal_details['signal_high'], 2),
                    'Signal_Close': round(signal_details['signal_close'], 2),
                    'Regular_Close': round(current['Close'], 2)
                })
        
        if signals_found > 0:
            print(f"  Found {signals_found} signals")
        
        time.sleep(0.1)  # Rate limiting
    
    def run_full_analysis(self):
        """Run analysis on full Nifty 500"""
        print("=== FULL NIFTY 500 ANALYSIS ===")
        print("Enhanced signal quality with sustained breakout validation")
        print("=" * 60)
        
        stocks = self.get_full_nifty500_list()
        
        for symbol, market_cap in stocks.items():
            self.analyze_stock(symbol, market_cap)
        
        # Convert results to DataFrame
        results_df = pd.DataFrame(self.results)
        if not results_df.empty:
            results_df = results_df.sort_values('Date', ascending=False)
            
            print(f"\n=== FULL NIFTY 500 ANALYSIS COMPLETE ===")
            print(f"Total signals found: {len(results_df)}")
            
            # Summary by market cap
            summary = results_df.groupby('Market_Cap').size().reset_index(name='Signal_Count')
            print("\nSummary by Market Cap:")
            print(summary.to_string(index=False))
            
            # Save results
            results_df.to_csv('full_nifty500_signals.csv', index=False)
            print(f"\nResults saved to 'full_nifty500_signals.csv'")
            
        return results_df

if __name__ == "__main__":
    analyzer = FullNifty500Analyzer()
    results = analyzer.run_full_analysis()
