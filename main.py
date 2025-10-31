# -*- coding: utf-8 -*-

"""
Ponto de entrada principal para o processo de backtest.

Este script orquestra o download dos dados, a execução dos cenários de backtest,
o salvamento dos resultados e a plotagem dos gráficos.
"""

import warnings
import os
import pandas as pd

# Importa as configurações e os novos módulos
import config
import data_loader
import scenarios
import plotting

def save_results_to_excel(lump_sum_results, monthly_results, monthly_contributions, cdb_results, cdb_contributions):
    """Salva os resultados dos backtests em arquivos Excel separados na pasta /results."""
    print("\nSalvando resultados em Excel...")
    
    if not os.path.exists('results'):
        os.makedirs('results')
        
    path_lump_sum = os.path.join('results', config.ARQUIVO_RESULTADOS_APORTE_UNICO)
    path_monthly = os.path.join('results', config.ARQUIVO_RESULTADOS_APORTES_MENSAIS)
    path_cdb = os.path.join('results', config.ARQUIVO_RESULTADOS_APORTES_CDB)
    
    try:
        with pd.ExcelWriter(path_lump_sum) as writer:
            lump_sum_results.resample('M').last().to_excel(writer, sheet_name='Aporte Unico (Mensal)')
        print(f"Resultados do Aporte Único salvos em '{path_lump_sum}'")

        with pd.ExcelWriter(path_monthly) as writer:
            monthly_results.resample('M').last().to_excel(writer, sheet_name='Aportes Mensais (Mensal)')
            monthly_contributions.iloc[[-1]].to_excel(writer, sheet_name='Aportes Acumulados')
        print(f"Resultados dos Aportes Mensais salvos em '{path_monthly}'")

        with pd.ExcelWriter(path_cdb) as writer:
            cdb_results.resample('M').last().to_excel(writer, sheet_name='Aportes CDB Misto (Mensal)')
            cdb_contributions.iloc[[-1]].to_excel(writer, sheet_name='Aportes Acumulados')
        print(f"Resultados dos Aportes CDB Misto salvos em '{path_cdb}'")
    except Exception as e:
        print(f"ERRO ao salvar resultados em Excel: {e}")

def main():
    """Função principal que orquestra o processo de backtest."""
    warnings.simplefilter(action='ignore', category=FutureWarning)

    tickers_sa = config.TICKERS_EMPRESAS
    data_inicio = config.DATA_INICIO
    data_fim = config.DATA_FIM

    data_historica, failed_tickers = data_loader.download_stock_data(tickers_sa, data_inicio, data_fim)
    
    if failed_tickers:
        print("\n--- Tickers que falharam no download ---")
        for ticker in failed_tickers:
            print(ticker)
        print("----------------------------------------")

    if data_historica is None:
        return

    benchmark_df = data_loader.get_benchmark_data(data_inicio, data_fim)
    ipca_df = data_loader.get_ipca_data(data_inicio, data_fim)

    benchmark_diaria, ipca_mensal = data_loader.prepare_benchmark_data(benchmark_df, ipca_df)

    lump_sum_results = scenarios.run_lump_sum_backtest(data_historica, benchmark_diaria, ipca_mensal, tickers_sa, data_inicio, data_fim)
    monthly_results, monthly_contributions = scenarios.run_monthly_contributions_backtest(data_historica, benchmark_diaria, ipca_mensal, tickers_sa, data_inicio, data_fim)
    cdb_results, cdb_contributions = scenarios.run_scenario_cdb_mixed(data_inicio, data_fim, config.APORTE_MENSAL_BASE, data_historica, benchmark_diaria, ipca_mensal, config.CDB_PERCENTAGE)

    if lump_sum_results is not None and monthly_results is not None and cdb_results is not None:
        save_results_to_excel(lump_sum_results, monthly_results, monthly_contributions, cdb_results, cdb_contributions)
        plotting.plot_results(lump_sum_results, monthly_results, monthly_contributions, cdb_results, cdb_contributions)
    else:
        print("\nAVISO: Nenhum resultado foi gerado. Gráficos e salvamento em Excel foram ignorados.")

if __name__ == "__main__":
    main()
