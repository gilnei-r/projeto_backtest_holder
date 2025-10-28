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

def save_results_to_excel(lump_sum_results, monthly_results):
    """Salva os resultados dos backtests em arquivos Excel separados na pasta /results."""
    print("\nSalvando resultados em Excel...")
    
    # Garante que o diretório de resultados exista
    if not os.path.exists('results'):
        os.makedirs('results')
        
    path_lump_sum = os.path.join('results', config.ARQUIVO_RESULTADOS_APORTE_UNICO)
    path_monthly = os.path.join('results', config.ARQUIVO_RESULTADOS_APORTES_MENSAIS)
    
    try:
        with pd.ExcelWriter(path_lump_sum) as writer:
            lump_sum_results.resample('M').last().to_excel(writer, sheet_name='Aporte Unico (Mensal)')
        print(f"Resultados do Aporte Único salvos em '{path_lump_sum}'")

        with pd.ExcelWriter(path_monthly) as writer:
            monthly_results.resample('M').last().to_excel(writer, sheet_name='Aportes Mensais (Mensal)')
        print(f"Resultados dos Aportes Mensais salvos em '{path_monthly}'")
    except Exception as e:
        print(f"ERRO ao salvar resultados em Excel: {e}")

def main():
    """Função principal que orquestra o processo de backtest."""
    warnings.simplefilter(action='ignore', category=FutureWarning)

    # Carrega configuração
    tickers_sa = config.TICKERS_EMPRESAS
    data_inicio = config.DATA_INICIO
    data_fim = config.DATA_FIM

    # --- Download de Todos os Dados ---
    data_historica = data_loader.download_stock_data(tickers_sa, data_inicio, data_fim)
    if data_historica is None:
        return # Encerra se não houver dados de ações

    selic_df = data_loader.get_selic_data(data_inicio, data_fim)
    ipca_df = data_loader.get_ipca_data(data_inicio, data_fim)

    # --- Preparação dos Dados de Benchmark ---
    selic_diaria, ipca_mensal = data_loader.prepare_benchmark_data(selic_df, ipca_df)

    # --- Execução dos Cenários de Backtest ---
    lump_sum_results = scenarios.run_lump_sum_backtest(data_historica, selic_diaria, ipca_mensal, tickers_sa, data_inicio, data_fim)
    monthly_results = scenarios.run_monthly_contributions_backtest(data_historica, selic_diaria, ipca_mensal, tickers_sa, data_inicio, data_fim)

    # --- Salvamento e Visualização ---
    if lump_sum_results is not None and monthly_results is not None:
        save_results_to_excel(lump_sum_results, monthly_results)
        plotting.plot_results(lump_sum_results, monthly_results)
    else:
        print("\nAVISO: Nenhum resultado foi gerado. Gráficos e salvamento em Excel foram ignorados.")

if __name__ == "__main__":
    main()
