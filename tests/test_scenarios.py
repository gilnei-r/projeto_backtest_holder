import unittest
import pandas as pd
import numpy as np
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scenarios import run_scenario_cdb_mixed, calculate_ipca_benchmark
import config

class TestCDBScenario(unittest.TestCase):

    def setUp(self):
        """Set up mock data for the tests."""
        self.start_date = '2020-01-01'
        self.end_date = '2020-03-31'
        self.monthly_contribution = 1000.0
        self.cdb_percentage = 0.5  # 50%

        # Mock tickers
        config.TICKERS_EMPRESAS = ['TICKER_A.SA', 'TICKER_B.SA']

        # Mock portfolio data
        dates = pd.date_range(self.start_date, self.end_date, freq='D')
        columns = pd.MultiIndex.from_product([['Close', 'Dividends'], config.TICKERS_EMPRESAS], names=['Attributes', 'Symbols'])
        self.portfolio_data = pd.DataFrame(index=dates, columns=columns)
        # Set Close prices
        self.portfolio_data[('Close', 'TICKER_A.SA')] = 10.0
        self.portfolio_data[('Close', 'TICKER_B.SA')] = 20.0 # Make Ticker B more expensive
        # Set Dividends to 0
        self.portfolio_data[('Dividends', 'TICKER_A.SA')] = 0.0
        self.portfolio_data[('Dividends', 'TICKER_B.SA')] = 0.0

        # Mock SELIC and IPCA data
        self.benchmark_data = pd.Series(1.0001, index=dates) # Small daily interest
        self.ipca_data = pd.Series(0.005, index=pd.to_datetime(['2020-01-31', '2020-02-29', '2020-03-31'])) # 0.5% monthly inflation

    def test_allocation_to_cdb_when_below_target(self):
        """Verify that the contribution goes to CDB when its allocation is below the target."""
        # In the first month, CDB value is 0, so it should receive the contribution.
        results = run_scenario_cdb_mixed(
            self.start_date, self.end_date, self.monthly_contribution, 
            self.portfolio_data, self.benchmark_data, self.ipca_data, self.cdb_percentage
        )
        
        # Find the first contribution
        first_contribution_date = results[results['Aporte'] > 0].index[0]
        
        self.assertEqual(results.loc[first_contribution_date, 'Ativo Aportado'], 'CDB')

    def test_allocation_to_stock_when_cdb_above_target(self):
        """Verify that the contribution goes to the lowest value stock when CDB is above target."""
        low_cdb_percentage = 0.1 # 10%
        results_low_cdb = run_scenario_cdb_mixed(
            self.start_date, self.end_date, self.monthly_contribution, 
            self.portfolio_data, self.benchmark_data, self.ipca_data, low_cdb_percentage
        )
        
        contribution_dates = results_low_cdb[results_low_cdb['Aporte'] > 0].index
        second_contribution_date = contribution_dates[1]

        self.assertEqual(results_low_cdb.loc[second_contribution_date, 'Ativo Aportado'], 'TICKER_A.SA')

class TestIPCABenchmark(unittest.TestCase):

    def setUp(self):
        """Set up mock data for the IPCA benchmark test."""
        self.start_date = '2020-01-01'
        self.end_date = '2020-03-31'
        dates = pd.date_range(self.start_date, self.end_date, freq='D')
        self.portfolio_df = pd.DataFrame(index=dates)
        self.ipca_mensal = pd.Series([0.5, 0.4, 0.6], index=pd.to_datetime(['2020-01-31', '2020-02-29', '2020-03-31']))
        self.initial_investment = 1000

    def test_ipca_benchmark_monthly_adjustment(self):
        """Verify that the IPCA benchmark value changes only on the last day of the month."""
        
        # Set IPCA_BENCHMARK_X to 0 to isolate the IPCA effect
        config.IPCA_BENCHMARK_X = 0.0

        result_df = calculate_ipca_benchmark(self.portfolio_df.copy(), self.ipca_mensal, self.initial_investment)

        # Check that the value is constant within each month, except for the last day
        for month in [1, 2, 3]:
            month_data = result_df[result_df.index.month == month]
            # The value should only change on the last day. So all days except the last should be the same.
            # And the last day should be different from the first day of the same month.
            if len(month_data) > 1:
                first_day_value = month_data['IPCA_Benchmark'].iloc[0]
                last_day_value = month_data['IPCA_Benchmark'].iloc[-1]
                # Check that all values before the last day are the same
                self.assertTrue((month_data['IPCA_Benchmark'][:-1].round(5) == round(first_day_value, 5)).all())
                # Check that the value on the last day is different (it has the IPCA adjustment)
                self.assertNotEqual(round(first_day_value, 5), round(last_day_value, 5))

if __name__ == '__main__':
    unittest.main()