import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
from datetime import datetime, timedelta

# Add the project root to the Python path to allow importing from the main project
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_loader import (
    _is_cache_valid,
    download_stock_data,
    get_ipca_data,
    get_selic_data
)
from config import DATA_UPDATE_DAYS

class TestDataCaching(unittest.TestCase):

    def setUp(self):
        """Set up a dummy data directory for tests."""
        self.test_data_dir = 'data'
        os.makedirs(self.test_data_dir, exist_ok=True)

    @patch('data_loader.os.path.getmtime')
    @patch('data_loader.os.path.exists')
    def test_is_cache_valid_fresh(self, mock_exists, mock_getmtime):
        """Test that _is_cache_valid returns True for a recent file."""
        mock_exists.return_value = True
        mock_getmtime.return_value = datetime.now().timestamp()
        self.assertTrue(_is_cache_valid('dummy/path.csv'))

    @patch('data_loader.os.path.getmtime')
    @patch('data_loader.os.path.exists')
    def test_is_cache_valid_stale(self, mock_exists, mock_getmtime):
        """Test that _is_cache_valid returns False for an old file."""
        mock_exists.return_value = True
        stale_time = (datetime.now() - timedelta(days=DATA_UPDATE_DAYS + 1)).timestamp()
        mock_getmtime.return_value = stale_time
        self.assertFalse(_is_cache_valid('dummy/path.csv'))

    @patch('data_loader.os.path.exists')
    def test_is_cache_valid_no_file(self, mock_exists):
        """Test that _is_cache_valid returns False if the file does not exist."""
        mock_exists.return_value = False
        self.assertFalse(_is_cache_valid('dummy/path.csv'))

    @patch('data_loader.yf.download')
    @patch('data_loader.pd.read_csv')
    @patch('data_loader._is_cache_valid')
    def test_download_stock_data_uses_cache(self, mock_is_cache_valid, mock_read_csv, mock_yf_download):
        """Verify stock download uses cache if valid."""
        mock_is_cache_valid.return_value = True
        # Mock the read_csv to return a valid DataFrame
        mock_read_csv.return_value = pd.DataFrame({'Close': [10, 11]})
        
        download_stock_data(['PETR4.SA'], '2020-01-01', '2020-01-31')
        
        mock_read_csv.assert_called_once_with('data/PETR4.SA.csv', index_col=0, parse_dates=True)
        mock_yf_download.assert_not_called()

    @patch('data_loader.yf.download')
    @patch('data_loader._is_cache_valid')
    def test_download_stock_data_downloads_when_no_cache(self, mock_is_cache_valid, mock_yf_download):
        """Verify stock download happens when cache is invalid."""
        mock_is_cache_valid.return_value = False
        # Mock the download to return a valid DataFrame
        mock_df = pd.DataFrame({'Close': [10, 11]})
        mock_yf_download.return_value = mock_df
        
        with patch.object(mock_df, 'to_csv') as mock_to_csv:
            download_stock_data(['PETR4.SA'], '2020-01-01', '2020-01-31')
            
            mock_yf_download.assert_called_once()
            mock_to_csv.assert_called_once_with('data/PETR4.SA.csv')

    @patch('data_loader.download_bcb_series')
    @patch('data_loader.pd.read_csv')
    @patch('data_loader._is_cache_valid')
    def test_get_ipca_data_uses_cache(self, mock_is_cache_valid, mock_read_csv, mock_download_bcb):
        """Verify IPCA download uses cache if valid."""
        mock_is_cache_valid.return_value = True
        
        get_ipca_data('2020-01-01', '2020-01-31')
        
        mock_read_csv.assert_called_once_with('data/IPCA.csv', index_col=0, parse_dates=True)
        mock_download_bcb.assert_not_called()

    @patch('data_loader.download_bcb_series')
    @patch('data_loader._is_cache_valid')
    def test_get_ipca_data_downloads_when_no_cache(self, mock_is_cache_valid, mock_download_bcb):
        """Verify IPCA download happens when cache is invalid."""
        mock_is_cache_valid.return_value = False
        mock_df = pd.DataFrame({'ipca': [0.5, 0.6]})
        mock_download_bcb.return_value = mock_df
        
        with patch.object(mock_df, 'to_csv') as mock_to_csv:
            get_ipca_data('2020-01-01', '2020-01-31')
            
            mock_download_bcb.assert_called_once()
            mock_to_csv.assert_called_once_with('data/IPCA.csv')

if __name__ == '__main__':
    unittest.main()