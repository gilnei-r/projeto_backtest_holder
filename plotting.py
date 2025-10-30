# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from config import BENCHMARK_NAME

def plot_ticker_distribution(monthly_results):
    """Gera um gráfico de barras com a distribuição de valor por ativo."""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Pega a última linha de dados para os valores finais
    final_values = monthly_results.iloc[-1]
    
    # Filtra para manter apenas os tickers, excluindo colunas de resumo
    tickers = [col for col in monthly_results.columns if '.SA' in col]
    ticker_values = final_values[tickers]
    
    # Ordena os valores em ordem decrescente
    sorted_ticker_values = ticker_values.sort_values(ascending=False)
    
    if not sorted_ticker_values.empty:
        sorted_ticker_values.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_title('Distribuição de Valor por Ativo no Final do Período', fontsize=18)
        ax.set_xlabel('Ativo')
        ax.set_ylabel('Valor Total (R$)')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))
        ax.tick_params(axis='x', rotation=45)
    else:
        ax.text(0.5, 0.5, 'Sem dados de valor de ticker para exibir.', horizontalalignment='center', verticalalignment='center')
        ax.set_title('Distribuição de Valor por Ativo', fontsize=18)

def plot_results(lump_sum_results, monthly_results, cdb_results):
    """Gera e exibe os gráficos dos resultados."""
    print("Gerando gráficos...")
    
    # Gráfico 1: Cenário de Aporte Único
    fig1, ax1 = plt.subplots(figsize=(14, 8))
    ax1.plot(lump_sum_results.index, lump_sum_results['Total'], label='Carteira', color='blue', linewidth=2)
    if BENCHMARK_NAME in lump_sum_results and not lump_sum_results[BENCHMARK_NAME].isna().all():
        ax1.plot(lump_sum_results.index, lump_sum_results[BENCHMARK_NAME], label=BENCHMARK_NAME, color='green', linestyle='--')
    if 'IPCA_Benchmark' in lump_sum_results and not lump_sum_results['IPCA_Benchmark'].isna().all():
        ax1.plot(lump_sum_results.index, lump_sum_results['IPCA_Benchmark'], label='IPCA + 6%', color='purple', linestyle='-.')
    ax1.set_title('Cenário 1: Curva de Capital com Aporte Único', fontsize=18)
    ax1.set_xlabel('Data'); ax1.set_ylabel('Valor da Carteira (R$)'); ax1.legend(loc='upper left')
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))

    # Gráfico 2: Cenário de Aportes Mensais
    fig2, ax2 = plt.subplots(figsize=(14, 8))
    ax2.plot(monthly_results.index, monthly_results['Total'], label='Carteira', color='blue', linewidth=2)
    if BENCHMARK_NAME in monthly_results and not monthly_results[BENCHMARK_NAME].isna().all():
        ax2.plot(monthly_results.index, monthly_results[BENCHMARK_NAME], label=BENCHMARK_NAME, color='green', linestyle='--')
    if 'IPCA_Benchmark' in monthly_results and not monthly_results['IPCA_Benchmark'].isna().all():
        ax2.plot(monthly_results.index, monthly_results['IPCA_Benchmark'], label='IPCA + 6%', color='purple', linestyle='-.')
    ax2.plot(monthly_results.index, monthly_results['Total Investido'], label='Total Investido', color='red', linestyle=':')
    ax2.set_title('Cenário 2: Curva de Capital com Aportes Mensais', fontsize=18)
    ax2.set_xlabel('Data'); ax2.set_ylabel('Valor da Carteira (R$)'); ax2.legend(loc='upper left')
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))

    # Gráfico 3: Cenário CDB Misto
    plot_cdb_mixed_scenario(cdb_results)

    # Gráfico 4: Distribuição de Aportes Mensais
    fig3, ax3 = plt.subplots(figsize=(14, 8))
    monthly_contributions = monthly_results['Ativo Aportado'].replace("", np.nan).resample('M').first().dropna()
    
    # Processa as entradas para lidar com múltiplos tickers por aporte
    all_individual_contributions = []
    for contribution_group in monthly_contributions:
        all_individual_contributions.extend(contribution_group.split(','))
    
    contribution_counts = pd.Series(all_individual_contributions).value_counts()
    if not contribution_counts.empty:
        contribution_counts.plot(kind='bar', ax=ax3, color='coral')
        ax3.set_title('Quantidade de Aportes Mensais por Ativo', fontsize=18)
        ax3.set_xlabel('Ativo'); ax3.set_ylabel('Número de Aportes')
        ax3.tick_params(axis='x', rotation=90)
    else:
        ax3.text(0.5, 0.5, 'Sem dados de aporte para exibir.', horizontalalignment='center', verticalalignment='center')
        ax3.set_title('Quantidade de Aportes Mensais por Ativo', fontsize=18)

    # Gráfico 5: Distribuição de Valor por Ativo
    plot_ticker_distribution(monthly_results)

    plt.tight_layout()
    plt.show()

def plot_cdb_mixed_scenario(results_df):
    """Gera o gráfico para o cenário de aportes com alocação em CDB."""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.plot(results_df.index, results_df['Total'], label='Carteira', color='blue', linewidth=2)
    if BENCHMARK_NAME in results_df and not results_df[BENCHMARK_NAME].isna().all():
        ax.plot(results_df.index, results_df[BENCHMARK_NAME], label=BENCHMARK_NAME, color='green', linestyle='--')
    if 'IPCA_Benchmark' in results_df and not results_df['IPCA_Benchmark'].isna().all():
        ax.plot(results_df.index, results_df['IPCA_Benchmark'], label='IPCA + 6%', color='purple', linestyle='-.')
    ax.plot(results_df.index, results_df['Total Investido'], label='Total Investido', color='red', linestyle=':')
    ax.set_title('Cenário 3: Curva de Capital com Aportes Mensais e Alocação em CDB', fontsize=18)
    ax.set_xlabel('Data'); ax.set_ylabel('Valor da Carteira (R$)'); ax.legend(loc='upper left')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))
