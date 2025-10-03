import pandas as pd
import numpy as np
from datetime import datetime
import time

def main():
    print("=== COMPLETE NIFTY 500 ANALYSIS & BACKTESTING ===")
    print("Phase 1: Full Nifty 500 Analysis")
    print("Phase 2: Comprehensive Backtesting")
    print("=" * 60)
    
    # Phase 1: Run Full Nifty 500 Analysis
    print("\nPHASE 1: FULL NIFTY 500 ANALYSIS")
    print("-" * 40)
    
    from full_nifty500_analyzer import FullNifty500Analyzer
    
    analyzer = FullNifty500Analyzer()
    signals_results = analyzer.run_full_analysis()
    
    if signals_results is None or signals_results.empty:
        print("No signals found. Cannot proceed with backtesting.")
        return
    
    print(f"\nPhase 1 Complete: {len(signals_results)} signals found")
    
    # Phase 2: Run Backtesting
    print("\nPHASE 2: COMPREHENSIVE BACKTESTING")
    print("-" * 40)
    
    from backtesting_framework import BacktestingFramework
    
    backtester = BacktestingFramework()
    backtest_results = backtester.run_backtest('full_nifty500_signals.csv')
    
    if backtest_results is None or backtest_results.empty:
        print("Backtesting failed.")
        return
    
    print(f"\nPhase 2 Complete: {len(backtest_results)} trades analyzed")
    
    # Phase 3: Generate Final Report
    print("\nPHASE 3: FINAL REPORT GENERATION")
    print("-" * 40)
    
    generate_final_report(signals_results, backtest_results)
    
    print("\nCOMPLETE ANALYSIS FINISHED!")
    print("=" * 60)
    print("Files Generated:")
    print("  - full_nifty500_signals.csv - All detected signals")
    print("  - backtest_results.csv - Detailed trade results")
    print("  - performance_summary.csv - Performance metrics")
    print("  - final_analysis_report.md - Comprehensive report")
    print("=" * 60)

def generate_final_report(signals_df, backtest_df):
    """Generate comprehensive final report"""
    
    report_content = f"""# Complete Nifty 500 Analysis & Backtesting Report

## Executive Summary

**Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Signals Detected**: {len(signals_df)}
**Total Trades Analyzed**: {len(backtest_df)}

## Signal Detection Results

### Market Cap Distribution
"""
    
    # Add market cap summary
    market_cap_summary = signals_df.groupby('Market_Cap').size().reset_index(name='Count')
    for _, row in market_cap_summary.iterrows():
        report_content += f"- **{row['Market_Cap']}**: {row['Count']} signals\n"
    
    # Add breakout strength analysis
    breakout_strengths = signals_df['Breakout_Strength_Percent']
    report_content += f"""
### Breakout Strength Analysis
- **Average Breakout Strength**: {breakout_strengths.mean():.2f}%
- **Strongest Breakout**: {breakout_strengths.max():.2f}%
- **Weakest Breakout**: {breakout_strengths.min():.2f}%

### Top 10 Strongest Breakouts
"""
    
    top_breakouts = signals_df.nlargest(10, 'Breakout_Strength_Percent')
    for _, signal in top_breakouts.iterrows():
        report_content += f"- **{signal['Stock_Ticker']}**: {signal['Breakout_Strength_Percent']:.2f}% ({signal['Date']})\n"
    
    # Add backtesting results
    completed_trades = backtest_df[backtest_df['status'] == 'Completed']
    if not completed_trades.empty:
        returns = completed_trades['return_percent']
        winning_trades = len(returns[returns > 0])
        
        report_content += f"""
## Backtesting Results

### Performance Metrics
- **Entry Success Rate**: {(len(completed_trades)/len(backtest_df))*100:.1f}%
- **Average Return**: {returns.mean():.2f}%
- **Win Rate**: {(winning_trades/len(completed_trades))*100:.1f}%
- **Best Trade**: {returns.max():.2f}%
- **Worst Trade**: {returns.min():.2f}%

### Exit Reason Distribution
"""
        
        exit_reasons = completed_trades['exit_reason'].value_counts()
        for reason, count in exit_reasons.items():
            report_content += f"- **{reason}**: {count} trades ({(count/len(completed_trades))*100:.1f}%)\n"
        
        # Add top performing trades
        report_content += f"""
### Top 10 Performing Trades
"""
        top_trades = completed_trades.nlargest(10, 'return_percent')
        for _, trade in top_trades.iterrows():
            report_content += f"- **{trade['symbol']}**: {trade['return_percent']:.2f}% ({trade['exit_reason']})\n"
    
    report_content += f"""
## Strategy Validation

### Entry Conditions
1. Cut high of signal candle
2. Above 21 EMA
3. All 7 improved signal criteria met

### Exit Conditions
1. **Stop Loss**: Monthly candle closes below 21 EMA
2. **Target 1**: First red long-legged doji Heikin Ashi
3. **Target 2**: Candle closes below 21 EMA from recent high

### Risk Management
- Systematic stop loss implementation
- Multiple target options for profit taking
- Monthly timeframe reduces noise

## Recommendations

### For Trading
1. **Prioritize strong breakouts** (top 10% by strength)
2. **Monitor 21 EMA** for stop loss and target 2
3. **Watch for doji patterns** for target 1
4. **Use position sizing** based on breakout strength

### For Investment
1. **Focus on large cap signals** for stability
2. **Consider sector diversification** across signals
3. **Long-term perspective** (average {completed_trades['months_held'].mean():.1f} months holding period)

## Files Generated
- `full_nifty500_signals.csv` - Complete signal database
- `backtest_results.csv` - Detailed trade analysis
- `performance_summary.csv` - Key performance metrics
- `final_analysis_report.md` - This comprehensive report

---
*Report generated by Nifty 500 Analysis & Backtesting Framework*
"""
    
    # Save report with UTF-8 encoding
    with open('final_analysis_report.md', 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print("Final report generated: final_analysis_report.md")

if __name__ == "__main__":
    main()
