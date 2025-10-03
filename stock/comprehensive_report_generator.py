import pandas as pd
import numpy as np
from datetime import datetime
import os

class ComprehensiveReportGenerator:
    def __init__(self):
        self.report_content = ""
        
    def generate_comprehensive_report(self, analysis_file):
        """Generate a comprehensive report with all metrics"""
        print("=== GENERATING COMPREHENSIVE REPORT ===")
        
        try:
            df = pd.read_csv(analysis_file)
        except FileNotFoundError:
            print(f"Analysis file {analysis_file} not found.")
            return None
        
        # Start building report
        self.report_content = f"""
# COMPREHENSIVE POSITION ANALYSIS REPORT
## Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## EXECUTIVE SUMMARY
- **Total Signals Analyzed**: {len(df)}
- **Completed Trades**: {len(df[df['status'] == 'Completed'])}
- **Success Rate**: {(len(df[df['status'] == 'Completed'])/len(df))*100:.1f}%

## DETAILED METRICS BY POSITION

| Symbol | Signal Date | Market Cap | Sector | Entry Price | Entry Date | Exit Price | Exit Date | Exit Reason | Months Held | Total Return % | CAGR % | CMGR % | Max High | Max High Date | Drawdown % | Stop Loss Price | Target 1 Price | Target 2 Price |
|--------|-------------|------------|--------|-------------|------------|------------|-----------|-------------|-------------|----------------|--------|--------|----------|---------------|------------|-----------------|----------------|-----------------|
"""
        
        # Add each position as a row
        for _, row in df.iterrows():
            self.report_content += f"| {row['symbol']} | {row['signal_date']} | {row['market_cap']} | {row['sector']} | {row['entry_price']} | {row['entry_date']} | {row['exit_price']} | {row['exit_date']} | {row['exit_reason']} | {row['months_held']} | {row['total_return_percent']} | {row['cagr_percent']} | {row['cmgr_percent']} | {row['max_high']} | {row['max_high_date']} | {row['drawdown_percent']} | {row['stop_loss_price']} | {row['target1_price']} | {row['target2_price']} |\n"
        
        # Add summary statistics
        completed_trades = df[df['status'] == 'Completed']
        if len(completed_trades) > 0:
            returns = completed_trades['total_return_percent']
            cagr_values = completed_trades['cagr_percent']
            drawdown_values = completed_trades['drawdown_percent']
            
            self.report_content += f"""

## SUMMARY STATISTICS

### RETURN ANALYSIS
- **Average Return**: {returns.mean():.2f}%
- **Median Return**: {returns.median():.2f}%
- **Best Return**: {returns.max():.2f}%
- **Worst Return**: {returns.min():.2f}%
- **Standard Deviation**: {returns.std():.2f}%

### CAGR ANALYSIS
- **Average CAGR**: {cagr_values.mean():.2f}%
- **Median CAGR**: {cagr_values.median():.2f}%
- **Best CAGR**: {cagr_values.max():.2f}%
- **Worst CAGR**: {cagr_values.min():.2f}%

### DRAWDOWN ANALYSIS
- **Average Drawdown**: {drawdown_values.mean():.2f}%
- **Median Drawdown**: {drawdown_values.median():.2f}%
- **Maximum Drawdown**: {drawdown_values.max():.2f}%
- **Minimum Drawdown**: {drawdown_values.min():.2f}%

### EXIT REASON ANALYSIS
"""
            
            exit_reasons = completed_trades['exit_reason'].value_counts()
            for reason, count in exit_reasons.items():
                self.report_content += f"- **{reason}**: {count} trades ({(count/len(completed_trades))*100:.1f}%)\n"
            
            self.report_content += f"""

### MARKET CAP ANALYSIS
"""
            market_cap_analysis = completed_trades.groupby('market_cap')['total_return_percent'].agg(['count', 'mean', 'median', 'std'])
            for market_cap, stats in market_cap_analysis.iterrows():
                self.report_content += f"- **{market_cap}**: {stats['count']} trades, Avg Return: {stats['mean']:.2f}%, Median: {stats['median']:.2f}%\n"
            
            self.report_content += f"""

### SECTOR ANALYSIS
"""
            sector_analysis = completed_trades.groupby('sector')['total_return_percent'].agg(['count', 'mean', 'median']).sort_values('mean', ascending=False)
            for sector, stats in sector_analysis.iterrows():
                self.report_content += f"- **{sector}**: {stats['count']} trades, Avg Return: {stats['mean']:.2f}%, Median: {stats['median']:.2f}%\n"
        
        # Save report
        report_filename = f"comprehensive_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(self.report_content)
        
        print(f"Comprehensive report saved: {report_filename}")
        return report_filename
    
    def generate_csv_summary(self, analysis_file):
        """Generate a summary CSV with key metrics"""
        try:
            df = pd.read_csv(analysis_file)
        except FileNotFoundError:
            print(f"Analysis file {analysis_file} not found.")
            return None
        
        completed_trades = df[df['status'] == 'Completed']
        
        # Create summary by market cap
        market_cap_summary = completed_trades.groupby('market_cap').agg({
            'total_return_percent': ['count', 'mean', 'median', 'std'],
            'cagr_percent': ['mean', 'median'],
            'drawdown_percent': ['mean', 'max']
        }).round(2)
        
        # Create summary by sector
        sector_summary = completed_trades.groupby('sector').agg({
            'total_return_percent': ['count', 'mean', 'median'],
            'cagr_percent': ['mean', 'median'],
            'drawdown_percent': ['mean', 'max']
        }).round(2)
        
        # Create exit reason summary
        exit_reason_summary = completed_trades['exit_reason'].value_counts().to_frame()
        exit_reason_summary.columns = ['count']
        exit_reason_summary['percentage'] = (exit_reason_summary['count'] / len(completed_trades) * 100).round(2)
        
        # Save summaries
        summary_filename = f"analysis_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with pd.ExcelWriter(summary_filename.replace('.csv', '.xlsx'), engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='All_Positions', index=False)
            market_cap_summary.to_excel(writer, sheet_name='Market_Cap_Summary')
            sector_summary.to_excel(writer, sheet_name='Sector_Summary')
            exit_reason_summary.to_excel(writer, sheet_name='Exit_Reason_Summary')
        
        print(f"Summary Excel file saved: {summary_filename.replace('.csv', '.xlsx')}")
        return summary_filename

if __name__ == "__main__":
    generator = ComprehensiveReportGenerator()
    
    # Check if we have the sample analysis file
    if os.path.exists('comprehensive_position_analysis.csv'):
        print("Generating report from sample analysis...")
        report_file = generator.generate_comprehensive_report('comprehensive_position_analysis.csv')
        summary_file = generator.generate_csv_summary('comprehensive_position_analysis.csv')
    else:
        print("No analysis file found. Please run the position analyzer first.")
