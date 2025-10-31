import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from plotting import plot_results
import config
import os
import matplotlib.pyplot as plt

class TestPlotting(unittest.TestCase):

    def setUp(self):
        self.plot_dir = 'test_plots'
        config.PLOT_DIR = self.plot_dir
        if not os.path.exists(self.plot_dir):
            os.makedirs(self.plot_dir)

    def tearDown(self):
        if os.path.exists(self.plot_dir):
            for f in os.listdir(self.plot_dir):
                os.remove(os.path.join(self.plot_dir, f))
            os.rmdir(self.plot_dir)

    def test_plot_results_save_plots(self):
        config.SAVE_PLOTS = True
        
        lump_sum_results = pd.DataFrame({'Total': [1000, 1100], 'CDI': [1000, 1050], 'IPCA_Benchmark': [1000, 1060]}, index=pd.to_datetime(['2021-01-01', '2021-01-02']))
        monthly_results = pd.DataFrame({'Total': [1000, 1100], 'CDI': [1000, 1050], 'IPCA_Benchmark': [1000, 1060], 'Total Investido': [1000, 1000], 'Ativo Aportado': ['PETR4.SA', 'VALE3.SA']}, index=pd.to_datetime(['2021-01-01', '2021-01-02']))
        cdb_results = pd.DataFrame({'Total': [1000, 1100], 'CDI': [1000, 1050], 'IPCA_Benchmark': [1000, 1060], 'Total Investido': [1000, 1000]}, index=pd.to_datetime(['2021-01-01', '2021-01-02']))
        
        plot_results(lump_sum_results, monthly_results, cdb_results)
        
        self.assertTrue(os.path.exists(os.path.join(self.plot_dir, 'cenario_1_aporte_unico.png')))
        self.assertTrue(os.path.exists(os.path.join(self.plot_dir, 'cenario_2_aportes_mensais.png')))
        self.assertTrue(os.path.exists(os.path.join(self.plot_dir, 'cenario_3_cdb_misto.png')))
        self.assertTrue(os.path.exists(os.path.join(self.plot_dir, 'distribuicao_aportes.png')))
        self.assertTrue(os.path.exists(os.path.join(self.plot_dir, 'distribuicao_valor.png')))

    @patch('plotting.plt.show')
    def test_plot_results_show_plots(self, mock_show):
        config.SAVE_PLOTS = False
        
        lump_sum_results = pd.DataFrame({'Total': [1000, 1100], 'CDI': [1000, 1050], 'IPCA_Benchmark': [1000, 1060]}, index=pd.to_datetime(['2021-01-01', '2021-01-02']))
        monthly_results = pd.DataFrame({'Total': [1000, 1100], 'CDI': [1000, 1050], 'IPCA_Benchmark': [1000, 1060], 'Total Investido': [1000, 1000], 'Ativo Aportado': ['PETR4.SA', 'VALE3.SA']}, index=pd.to_datetime(['2021-01-01', '2021-01-02']))
        cdb_results = pd.DataFrame({'Total': [1000, 1100], 'CDI': [1000, 1050], 'IPCA_Benchmark': [1000, 1060], 'Total Investido': [1000, 1000]}, index=pd.to_datetime(['2021-01-01', '2021-01-02']))
        
        plot_results(lump_sum_results, monthly_results, cdb_results)
        
        mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()