import pandas as pd

# Read the refined results
df = pd.read_csv('stocks/refined_nifty500_signals.csv')

print('=== REFINED ANALYSIS BREAKDOWN ===')
print(f'Total refined signals found: {len(df)}')
print(f'Unique stocks with signals: {df["Stock_Ticker"].nunique()}')
print()

print('=== WHAT WE ANALYZED ===')
print('• We analyzed 30 major Nifty 500 stocks in the sample')
print('• But only some stocks met ALL 5 refined criteria')
print()

print('=== STOCKS THAT MET ALL CRITERIA ===')
unique_stocks = df.groupby('Stock_Ticker').agg({
    'Market_Cap': 'first',
    'Date': ['count', 'min', 'max']
}).round(2)
unique_stocks.columns = ['Market_Cap', 'Signal_Count', 'First_Signal', 'Last_Signal']
print(unique_stocks.to_string())

print()
print('=== ANSWER TO YOUR QUESTION ===')
print(f'• This is a SAMPLE of 30 major Nifty 500 stocks')
print(f'• Out of these 30 stocks, only {df["Stock_Ticker"].nunique()} stocks met all criteria')
print(f'• These {df["Stock_Ticker"].nunique()} stocks generated {len(df)} total signals')
print()
print('• To get the FULL Nifty 500 list, we would need to run the analysis')
print('  on all 500 stocks, not just the 30 sample stocks')
print('• The refined criteria are very selective - most stocks will not meet them')

