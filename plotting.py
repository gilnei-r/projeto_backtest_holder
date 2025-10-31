# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from config import BENCHMARK_NAME
import os
import config

def plot_ticker_distribution(final_values, final_contributions, ax):
    """Gera um gráfico de barras com a distribuição de valor e aporte por ativo."""
    tickers = [col for col in final_values.index if '.SA' in col or col == 'CDB']
    
    data = {
        'Valor Atual': final_values[tickers],
        'Aporte Total': final_contributions[tickers]
    }
    
    df = pd.DataFrame(data).reset_index().rename(columns={'index': 'Ticker'})
    df_melted = df.melt(id_vars='Ticker', var_name='Tipo', value_name='Valor')
    
    # Ordena o dataframe para garantir que os tickers fiquem agrupados
    df_melted.sort_values(by='Ticker', inplace=True)

    if not df_melted.empty:
        sns.barplot(x='Ticker', y='Valor', hue='Tipo', data=df_melted, ax=ax)
        ax.set_title('Valor Atual vs Aporte Total por Ativo', fontsize=18)
        ax.set_xlabel('Ativo')
        ax.set_ylabel('Valor (R$)')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))
        ax.tick_params(axis='x', rotation=90)
        ax.legend(title='Tipo')
    else:
        ax.text(0.5, 0.5, 'Sem dados de valor de ticker para exibir.', horizontalalignment='center', verticalalignment='center')
        ax.set_title('Distribuição de Valor por Ativo', fontsize=18)

def plot_results(lump_sum_results, monthly_results, monthly_contributions, cdb_results, cdb_contributions):
    """Gera e salva os gráficos dos resultados."""
    print("Gerando gráficos...")
    
    if config.SAVE_PLOTS:
        os.makedirs(config.PLOT_DIR, exist_ok=True)

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
    if config.SAVE_PLOTS:
        fig1.savefig(os.path.join(config.PLOT_DIR, 'cenario_1_aporte_unico.png'))
        plt.close(fig1)

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
    if config.SAVE_PLOTS:
        fig2.savefig(os.path.join(config.PLOT_DIR, 'cenario_2_aportes_mensais.png'))
        plt.close(fig2)

    # Gráfico 3: Cenário CDB Misto
    fig3, ax3 = plt.subplots(figsize=(14, 8))
    plot_cdb_mixed_scenario(cdb_results, ax3)
    if config.SAVE_PLOTS:
        fig3.savefig(os.path.join(config.PLOT_DIR, 'cenario_3_cdb_misto.png'))
        plt.close(fig3)

    # Gráfico 4: Distribuição de Aportes Mensais
    fig4, ax4 = plt.subplots(figsize=(14, 8))
    monthly_contributions_plot_data = monthly_results['Ativo Aportado'].replace("", np.nan).resample('M').first().dropna()
    
    all_individual_contributions = []
    for contribution_group in monthly_contributions_plot_data:
        all_individual_contributions.extend(contribution_group.split(','))
    
    contribution_counts = pd.Series(all_individual_contributions).value_counts()
    if not contribution_counts.empty:
        contribution_counts.plot(kind='bar', ax=ax4, color='coral')
        ax4.set_title('Quantidade de Aportes Mensais por Ativo', fontsize=18)
        ax4.set_xlabel('Ativo'); ax4.set_ylabel('Número de Aportes')
        ax4.tick_params(axis='x', rotation=90)
    else:
        ax4.text(0.5, 0.5, 'Sem dados de aporte para exibir.', horizontalalignment='center', verticalalignment='center')
        ax4.set_title('Quantidade de Aportes Mensais por Ativo', fontsize=18)
    if config.SAVE_PLOTS:
        fig4.savefig(os.path.join(config.PLOT_DIR, 'distribuicao_aportes.png'))
        plt.close(fig4)

    # Gráfico 5: Distribuição de Valor por Ativo (Cenário 2)
    fig5, ax5 = plt.subplots(figsize=(14, 8))
    plot_ticker_distribution(monthly_results.iloc[-1], monthly_contributions.iloc[-1], ax5)
    if config.SAVE_PLOTS:
        fig5.savefig(os.path.join(config.PLOT_DIR, 'distribuicao_valor.png'))
        plt.close(fig5)

    # Gráfico 6: Distribuição de Valor por Ativo (Cenário 3)
    fig6, ax6 = plt.subplots(figsize=(14, 8))
    plot_ticker_distribution(cdb_results.iloc[-1], cdb_contributions.iloc[-1], ax6)
    if config.SAVE_PLOTS:
        fig6.savefig(os.path.join(config.PLOT_DIR, 'distribuicao_valor_cdb.png'))
        plt.close(fig6)

    if not config.SAVE_PLOTS:
        plt.tight_layout()
        plt.show()

def plot_cdb_mixed_scenario(results_df, ax):
    """Gera o gráfico para o cenário de aportes com alocação em CDB."""
    ax.plot(results_df.index, results_df['Total'], label='Carteira', color='blue', linewidth=2)
    if BENCHMARK_NAME in results_df and not results_df[BENCHMARK_NAME].isna().all():
        ax.plot(results_df.index, results_df[BENCHMARK_NAME], label=BENCHMARK_NAME, color='green', linestyle='--')
    if 'IPCA_Benchmark' in results_df and not results_df['IPCA_Benchmark'].isna().all():
        ax.plot(results_df.index, results_df['IPCA_Benchmark'], label='IPCA + 6%', color='purple', linestyle='-.')
    ax.plot(results_df.index, results_df['Total Investido'], label='Total Investido', color='red', linestyle=':')
    ax.set_title('Cenário 3: Curva de Capital com Aportes Mensais e Alocação em CDB', fontsize=18)
    ax.set_xlabel('Data'); ax.set_ylabel('Valor da Carteira (R$)'); ax.legend(loc='upper left')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))
