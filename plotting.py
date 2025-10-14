# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

def plot_results(lump_sum_results, monthly_results):
    """Gera e exibe os gráficos dos resultados."""
    print("Gerando gráficos...")
    
    # Gráfico 1: Cenário de Aporte Único
    fig1, ax1 = plt.subplots(figsize=(14, 8))
    ax1.plot(lump_sum_results.index, lump_sum_results['Total'], label='Carteira', color='blue', linewidth=2)
    if 'Selic' in lump_sum_results and not lump_sum_results['Selic'].isna().all():
        ax1.plot(lump_sum_results.index, lump_sum_results['Selic'], label='Selic', color='green', linestyle='--')
    ax1.set_title('Cenário 1: Curva de Capital com Aporte Único', fontsize=18)
    ax1.set_xlabel('Data'); ax1.set_ylabel('Valor da Carteira (R$)'); ax1.legend(loc='upper left')
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))

    # Gráfico 2: Cenário de Aportes Mensais
    fig2, ax2 = plt.subplots(figsize=(14, 8))
    ax2.plot(monthly_results.index, monthly_results['Total'], label='Carteira', color='blue', linewidth=2)
    if 'Selic' in monthly_results and not monthly_results['Selic'].isna().all():
        ax2.plot(monthly_results.index, monthly_results['Selic'], label='Selic', color='green', linestyle='--')
    ax2.plot(monthly_results.index, monthly_results['Total Investido'], label='Total Investido', color='red', linestyle=':')
    ax2.set_title('Cenário 2: Curva de Capital com Aportes Mensais', fontsize=18)
    ax2.set_xlabel('Data'); ax2.set_ylabel('Valor da Carteira (R$)'); ax2.legend(loc='upper left')
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))

    # Gráfico 3: Distribuição de Aportes Mensais
    fig3, ax3 = plt.subplots(figsize=(14, 8))
    monthly_contributions = monthly_results['Ativo Aportado'].replace("", np.nan).resample('M').first()
    contribution_counts = monthly_contributions.dropna().value_counts()
    if not contribution_counts.empty:
        contribution_counts.plot(kind='bar', ax=ax3, color='coral')
        ax3.set_title('Quantidade de Aportes Mensais por Ativo', fontsize=18)
        ax3.set_xlabel('Ativo'); ax3.set_ylabel('Número de Aportes')
        ax3.tick_params(axis='x', rotation=90)
    else:
        ax3.text(0.5, 0.5, 'Sem dados de aporte para exibir.', horizontalalignment='center', verticalalignment='center')
        ax3.set_title('Quantidade de Aportes Mensais por Ativo', fontsize=18)

    plt.tight_layout()
    plt.show()
