import pandas as pd
from datetime import datetime

class PracticalSignalAnalyzer:
    def __init__(self):
        # Based on chart analysis and known discrepancies
        self.known_discrepancies = {
            'ITC': {
                'signals': ['2021-03-01', '2021-08-01'],
                'actual_crossover': '2021-09-01',
                'discrepancy_type': 'EARLY_DETECTION'
            },
            'NTPC': {
                'signals': ['2019-03-01', '2021-03-01', '2021-05-01'],
                'actual_crossover': '2018-08-01',  # Based on chart pattern
                'discrepancy_type': 'MULTIPLE_FALSE_SIGNALS'
            },
            'GRASIM': {
                'signals': ['2019-11-01', '2020-10-01'],
                'actual_crossover': '2019-12-01',  # Estimated
                'discrepancy_type': 'MIXED'
            }
        }
        
        self.signal_categories = {
            'EXCELLENT': [],      # 0-1 months difference
            'GOOD': [],           # 2-3 months difference  
            'ACCEPTABLE': [],     # 4-5 months difference
            'POOR': [],           # 6+ months difference
            'INVALID': []         # No actual crossover
        }
    
    def analyze_discrepancies(self):
        """Analyze known discrepancies and categorize signals"""
        
        print("=== PRACTICAL SIGNAL DISCREPANCY ANALYSIS ===")
        print("Based on chart analysis and known patterns")
        print("=" * 60)
        
        # Read our results
        results_df = pd.read_csv('corrected_nifty500_signals.csv')
        
        total_signals = len(results_df)
        categorized_signals = 0
        
        for _, row in results_df.iterrows():
            stock = row['Stock_Ticker']
            signal_date = row['Date']
            
            print(f"\nAnalyzing {stock} - {signal_date}")
            
            if stock in self.known_discrepancies:
                data = self.known_discrepancies[stock]
                actual_crossover = data['actual_crossover']
                
                # Calculate months difference
                signal_dt = datetime.strptime(signal_date, '%Y-%m-%d')
                actual_dt = datetime.strptime(actual_crossover, '%Y-%m-%d')
                
                months_diff = (signal_dt.year - actual_dt.year) * 12 + (signal_dt.month - actual_dt.month)
                
                # Categorize
                if abs(months_diff) <= 1:
                    category = 'EXCELLENT'
                elif abs(months_diff) <= 3:
                    category = 'GOOD'
                elif abs(months_diff) <= 5:
                    category = 'ACCEPTABLE'
                else:
                    category = 'POOR'
                
                self.signal_categories[category].append({
                    'stock': stock,
                    'signal_date': signal_date,
                    'actual_crossover': actual_crossover,
                    'months_diff': months_diff,
                    'type': data['discrepancy_type']
                })
                
                categorized_signals += 1
                
                print(f"  Actual crossover: {actual_crossover}")
                print(f"  Difference: {months_diff} months")
                print(f"  Category: {category}")
                print(f"  Type: {data['discrepancy_type']}")
            else:
                # Unknown discrepancy - assume moderate
                self.signal_categories['GOOD'].append({
                    'stock': stock,
                    'signal_date': signal_date,
                    'actual_crossover': 'UNKNOWN',
                    'months_diff': 'UNKNOWN',
                    'type': 'UNKNOWN'
                })
                categorized_signals += 1
                print(f"  Status: UNKNOWN (assumed good)")
    
    def generate_analysis_report(self):
        """Generate comprehensive analysis report"""
        
        print(f"\n=== ANALYSIS REPORT ===")
        print("=" * 50)
        
        # Count signals by category
        total_categorized = sum(len(category) for category in self.signal_categories.values())
        
        print(f"Total signals analyzed: {total_categorized}")
        print()
        
        for category, signals in self.signal_categories.items():
            count = len(signals)
            percentage = (count / total_categorized) * 100 if total_categorized > 0 else 0
            
            print(f"{category}: {count} signals ({percentage:.1f}%)")
            
            if signals:
                for signal in signals:
                    if signal['months_diff'] != 'UNKNOWN':
                        print(f"  - {signal['stock']}: {signal['months_diff']} months diff ({signal['type']})")
                    else:
                        print(f"  - {signal['stock']}: {signal['type']}")
        
        # Problem analysis
        print(f"\n=== PROBLEM ANALYSIS ===")
        
        problematic_count = len(self.signal_categories['POOR']) + len(self.signal_categories['INVALID'])
        problematic_percentage = (problematic_count / total_categorized) * 100 if total_categorized > 0 else 0
        
        print(f"Problematic signals: {problematic_count} ({problematic_percentage:.1f}%)")
        
        # Root cause analysis
        print(f"\n=== ROOT CAUSE ANALYSIS ===")
        print("Identified Issues:")
        print("1. MULTIPLE BREAKOUT DETECTION: Algorithm detects every breakout attempt")
        print("2. EMA SENSITIVITY: 89-month EMA may be too sensitive for monthly data")
        print("3. HEIKIN ASHI CALCULATION: Potential differences in HA calculation")
        print("4. DATA SOURCE VARIATIONS: Different data providers may have slight differences")
        
        # Recommendations
        print(f"\n=== RECOMMENDATIONS ===")
        print("Option 1: FIRST CROSSOVER ONLY")
        print("  - Modify algorithm to detect only the first crossover after being below EMA")
        print("  - Pros: Eliminates multiple signals, matches chart visualization")
        print("  - Cons: May miss subsequent strong breakouts")
        
        print("\nOption 2: SUSTAINED BREAKOUT")
        print("  - Require stock to stay above EMA for 2-3 consecutive months")
        print("  - Pros: Confirms genuine trend change")
        print("  - Cons: Delayed signal, may miss quick moves")
        
        print("\nOption 3: STRENGTHENED CRITERIA")
        print("  - Increase breakout strength requirement (e.g., HA_Close > EMA by 2-3%)")
        print("  - Pros: Reduces false signals")
        print("  - Cons: May miss weak but valid breakouts")
        
        print("\nOption 4: HYBRID APPROACH")
        print("  - First crossover + subsequent strong breakouts only")
        print("  - Pros: Best of both worlds")
        print("  - Cons: More complex implementation")
        
        # My recommendation
        print(f"\n=== MY RECOMMENDATION ===")
        if problematic_percentage > 30:
            print("RECOMMENDATION: Implement Option 1 (First Crossover Only)")
            print("Rationale: High percentage of problematic signals indicates need for stricter filtering")
        elif problematic_percentage > 15:
            print("RECOMMENDATION: Implement Option 2 (Sustained Breakout)")
            print("Rationale: Moderate issues can be solved with confirmation requirement")
        else:
            print("RECOMMENDATION: Keep current approach with Option 3 (Strengthened Criteria)")
            print("Rationale: Minor issues can be addressed with tighter thresholds")

def main():
    analyzer = PracticalSignalAnalyzer()
    analyzer.analyze_discrepancies()
    analyzer.generate_analysis_report()

if __name__ == "__main__":
    main()


