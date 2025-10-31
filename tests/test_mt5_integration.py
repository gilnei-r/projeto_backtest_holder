import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from data_loader import connect_mt5, download_mt5_data
import config

class TestMt5Integration(unittest.TestCase):

    @patch('data_loader.mt5')
    def test_connect_mt5_success(self, mock_mt5):
        mock_mt5.initialize.return_value = True
        self.assertTrue(connect_mt5())

    @patch('data_loader.mt5')
    def test_connect_mt5_failure(self, mock_mt5):
        mock_mt5.initialize.return_value = False
        config.MT5_RETRIES = 2
        config.MT5_TIMEOUT = 0.1
        self.assertFalse(connect_mt5())

    @patch('data_loader.connect_mt5')
    @patch('data_loader.mt5')
    def test_download_mt5_data_success(self, mock_mt5, mock_connect_mt5):
        import numpy as np
        mock_connect_mt5.return_value = True
        rates = np.array([(1609459200, 100.0, 102.0, 99.0, 101.0, 1000, 0, 0),
                          (1609545600, 101.0, 103.0, 100.0, 102.0, 1200, 0, 0)],
                         dtype=[('time', '<i8'), ('open', '<f8'), ('high', '<f8'), ('low', '<f8'), ('close', '<f8'), ('tick_volume', '<u8'), ('spread', '<i4'), ('real_volume', '<u8')])
        mock_mt5.copy_rates_from_pos.return_value = rates
        
        df = download_mt5_data('PETR4.SA', '2021-01-01', '2021-01-02')
        
        self.assertIsNotNone(df)
        self.assertEqual(len(df), 2)

    @patch('data_loader.connect_mt5')
    @patch('data_loader.mt5')
    def test_download_mt5_data_no_data(self, mock_mt5, mock_connect_mt5):
        mock_connect_mt5.return_value = True
        mock_mt5.copy_rates_from_pos.return_value = None
        
        df = download_mt5_data('PETR4.SA', '2021-01-01', '2021-01-02')
        
        self.assertIsNone(df)

if __name__ == '__main__':
    unittest.main()
