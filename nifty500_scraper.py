import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_nifty500_list():
    """Scrape Nifty 500 stock list from NSE website"""
    print("Fetching Nifty 500 stock list from NSE...")
    
    try:
        # NSE Nifty 500 URL
        url = "https://www.nseindia.com/market-data/live-equity-market"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        session = requests.Session()
        session.headers.update(headers)
        
        # Get the main page first to establish session
        response = session.get("https://www.nseindia.com/")
        time.sleep(2)
        
        # Now get the Nifty 500 data
        nifty500_url = "https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O"
        response = session.get(nifty500_url)
        
        if response.status_code == 200:
            data = response.json()
            stocks = []
            
            for item in data.get('data', []):
                symbol = item.get('symbol', '')
                if symbol:
                    stocks.append(symbol + '.NS')
            
            print(f"Successfully fetched {len(stocks)} stocks from Nifty 500")
            return stocks[:500]  # Limit to 500 stocks
            
    except Exception as e:
        print(f"Error fetching Nifty 500 list: {e}")
        print("Using fallback list...")
        
        # Fallback list of major Nifty 500 stocks
        fallback_stocks = [
            'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS',
            'ITC.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'KOTAKBANK.NS', 'LT.NS',
            'HDFC.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'MARUTI.NS', 'SUNPHARMA.NS',
            'ULTRACEMCO.NS', 'WIPRO.NS', 'NESTLEIND.NS', 'TITAN.NS', 'POWERGRID.NS',
            'NTPC.NS', 'ONGC.NS', 'COALINDIA.NS', 'TECHM.NS', 'BAJFINANCE.NS',
            'TATAMOTORS.NS', 'JSWSTEEL.NS', 'ADANIPORTS.NS', 'GRASIM.NS', 'CIPLA.NS',
            'DRREDDY.NS', 'BAJAJFINSV.NS', 'HINDALCO.NS', 'EICHERMOT.NS', 'APOLLOHOSP.NS',
            'BAJAJ-AUTO.NS', 'BRITANNIA.NS', 'DIVISLAB.NS', 'HEROMOTOCO.NS', 'HINDZINC.NS',
            'ICICIBANK.NS', 'INDUSINDBK.NS', 'M&M.NS', 'SHREECEM.NS', 'TATASTEEL.NS',
            'TATACONSUM.NS', 'HCLTECH.NS', 'SBILIFE.NS', 'ADANIGREEN.NS', 'ADANITRANS.NS',
            'UPL.NS', 'BPCL.NS', 'IOC.NS', 'GAIL.NS', 'VEDL.NS'
        ]
        return fallback_stocks

def classify_market_cap(symbol):
    """Classify stocks into Large/Mid/Small cap based on typical market cap ranges"""
    # This is a simplified classification - in practice you'd use actual market cap data
    
    large_cap_symbols = [
        'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS',
        'ITC.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'KOTAKBANK.NS', 'LT.NS',
        'HDFC.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'MARUTI.NS', 'SUNPHARMA.NS',
        'ULTRACEMCO.NS', 'WIPRO.NS', 'NESTLEIND.NS', 'TITAN.NS', 'POWERGRID.NS',
        'NTPC.NS', 'ONGC.NS', 'COALINDIA.NS', 'TECHM.NS', 'BAJFINANCE.NS',
        'ICICIBANK.NS', 'INDUSINDBK.NS', 'M&M.NS', 'SHREECEM.NS', 'TATASTEEL.NS',
        'TATACONSUM.NS', 'HCLTECH.NS', 'SBILIFE.NS', 'BPCL.NS', 'IOC.NS'
    ]
    
    mid_cap_symbols = [
        'TATAMOTORS.NS', 'JSWSTEEL.NS', 'ADANIPORTS.NS', 'GRASIM.NS', 'CIPLA.NS',
        'DRREDDY.NS', 'BAJAJFINSV.NS', 'HINDALCO.NS', 'EICHERMOT.NS', 'APOLLOHOSP.NS',
        'BAJAJ-AUTO.NS', 'BRITANNIA.NS', 'DIVISLAB.NS', 'HEROMOTOCO.NS', 'HINDZINC.NS',
        'ADANIGREEN.NS', 'ADANITRANS.NS', 'UPL.NS', 'GAIL.NS', 'VEDL.NS'
    ]
    
    if symbol in large_cap_symbols:
        return 'Large Cap'
    elif symbol in mid_cap_symbols:
        return 'Mid Cap'
    else:
        return 'Small Cap'

if __name__ == "__main__":
    stocks = get_nifty500_list()
    print(f"Total stocks: {len(stocks)}")
    
    # Test market cap classification
    for stock in stocks[:10]:
        cap = classify_market_cap(stock)
        print(f"{stock}: {cap}")

