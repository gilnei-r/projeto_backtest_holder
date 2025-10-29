import unittest
import pandas as pd
import numpy as np
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scenarios import run_scenario_cdb_mixed
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
        self.portfolio_data = pd.DataFrame(10.0, index=dates, columns=columns)
        self.portfolio_data[('Close', 'TICKER_B.SA')] = 20.0 # Make Ticker B more expensive

        # Mock SELIC and IPCA data
        self.selic_data = pd.Series(1.0001, index=dates) # Small daily interest
        self.ipca_data = pd.Series(0.005, index=dates) # 0.5% monthly inflation

    def test_allocation_to_cdb_when_below_target(self):
        """Verify that the contribution goes to CDB when its allocation is below the target."""
        # In the first month, CDB value is 0, so it should receive the contribution.
        results = run_scenario_cdb_mixed(
            self.start_date, self.end_date, self.monthly_contribution, 
            self.portfolio_data, self.selic_data, self.ipca_data, self.cdb_percentage
        )
        
        # Find the first contribution
        first_contribution_date = results[results['Aporte'] > 0].index[0]
        
        self.assertEqual(results.loc[first_contribution_date, 'Ativo Aportado'], 'CDB')

        def test_allocation_to_stock_when_cdb_above_target(self):
            """Verify that the contribution goes to the lowest value stock when CDB is above target."""
            low_cdb_percentage = 0.1 # 10%
            results_low_cdb = run_scenario_cdb_mixed(
                self.start_date, self.end_date, self.monthly_contribution, 
                self.portfolio_data, self.selic_data, self.ipca_data, low_cdb_percentage
            )
            
            contribution_dates = results_low_cdb[results_low_cdb['Aporte'] > 0].index
            second_contribution_date = contribution_dates[1]
    
                    self.assertEqual(results_low_cdb.loc[second_contribution_date, 'Ativo Aportado'], 'TICKER_A.SA')if __name__ == '__main__':
    unittest.main()