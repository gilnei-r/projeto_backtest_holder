# -*- coding: utf-8 -*-

"""
BACKTEST DE ESTRATÉGIAS DE INVESTIMENTO

Este script realiza o backtest de duas estratégias de investimento em ações brasileiras:
1. Aporte Único (Lump-Sum): Investe um valor fixo no início e o mantém (buy and hold).
2. Aportes Mensais: Realiza aportes mensais corrigidos pela inflação, investindo no
   ativo com menor valorização na carteira.

O desempenho é comparado com os benchmarks Selic e IMA-B 5+.

Para configurar os parâmetros do backtest, modifique o arquivo `config.py`.
"""

import time
import warnings
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import yfinance as yf
from bcb import sgs

# Importa as configurações do arquivo config.py
import config

# --- Funções Auxiliares ---

def calculate_cagr(start_value, end_value, years):
    """Calcula a Taxa de Crescimento Anual Composta (CAGR)."""
    if start_value == 0 or years <= 0:
        return 0
    return (end_value / start_value) ** (1 / years) - 1

def download_bcb_series(series_code, series_name, start_date, end_date, chunk_years=3):
    """Baixa séries temporais do BCB com lógica de retentativa e chunking."""
    print(f"Baixando dados para {series_name}...")
    chunks = []
    temp_start = pd.to_datetime(start_date)
    end_date_dt = pd.to_datetime(end_date)

    chunk_count = 0
    while temp_start < end_date_dt:
        temp_end = temp_start + pd.DateOffset(years=chunk_years)
        if temp_end > end_date_dt:
            temp_end = end_date_dt

        chunk_count += 1
        print(f"  Chunk {chunk_count}: {temp_start.strftime('%Y-%m-%d')} a {temp_end.strftime('%Y-%m-%d')}")

        for attempt in range(3):
            try:
                chunk = sgs.get({series_name: series_code}, start=temp_start.strftime('%Y-%m-%d'), end=temp_end.strftime('%Y-%m-%d'))
                if not chunk.empty:
                    chunks.append(chunk)
                    print(f"  OK: {len(chunk)} registros baixados")
                break
            except Exception as e:
                print(f"  Tentativa {attempt + 1} falhou: {str(e)[:80]}")
                if attempt < 2:
                    time.sleep(2)
                else:
                    print(f"  ERRO: Falha apos 3 tentativas")
                    break

        temp_start = temp_end + pd.DateOffset(days=1)

    if not chunks:
        print(f"ERRO: Nenhum dado foi baixado para {series_name}")
        return None

    full_df = pd.concat(chunks)
    full_df = full_df[~full_df.index.duplicated(keep='first')]
    print(f"Total: {len(full_df)} registros para {series_name}")
    return full_df

def run_lump_sum_backtest(data_historica, selic_diaria, imab_diario_ret, tickers_sa, data_inicio, data_fim):
    """Executa o backtest para o cenário de Aporte Único."""
    print("\n--- CENÁRIO 1: APORTE ÚNICO INICIAL ---")
    all_dates = pd.date_range(start=data_inicio, end=data_fim, freq='D')
    curva_de_capital = pd.DataFrame(index=all_dates)
    valid_tickers = [col for col in tickers_sa if col in data_historica['Close'].columns and not data_historica['Close'][col].dropna().empty]

    num_empresas = len(valid_tickers)
    investimento_total_inicial = config.VALOR_INVESTIDO_POR_EMPRESA * num_empresas

    print("Processando backtest para cada empresa...")
    for ticker in valid_tickers:
        stock_data = data_historica.loc[:, (slice(None), ticker)]
        stock_data.columns = stock_data.columns.droplevel(1)
        
        num_shares = config.VALOR_INVESTIDO_POR_EMPRESA / stock_data['Close'].iloc[0]
        daily_value = pd.Series(index=all_dates, dtype=float)

        for date, row in stock_data.iterrows():
            if 'Dividends' in row and row['Dividends'] > 0:
                num_shares += (num_shares * row['Dividends']) / row['Close']
            daily_value[date] = num_shares * row['Close']
        
        curva_de_capital[ticker] = daily_value.ffill()

    curva_de_capital.fillna(0, inplace=True)
    curva_de_capital['Total'] = curva_de_capital[valid_tickers].sum(axis=1)

    if selic_diaria is not None:
        selic_acumulada = selic_diaria.cumprod()
        curva_de_capital['Selic'] = investimento_total_inicial * selic_acumulada.reindex(all_dates, method='ffill')
    if imab_diario_ret is not None:
        imab_norm = (1 + imab_diario_ret).cumprod()
        curva_de_capital['IMA-B'] = investimento_total_inicial * imab_norm.reindex(all_dates, method='ffill')

    anos = (pd.to_datetime(data_fim) - pd.to_datetime(data_inicio)).days / 365.25
    valor_final_carteira = curva_de_capital['Total'].iloc[-1]
    print("\n--- Resultados do Backtest (Aporte Único) ---")
    print(f"Período: {data_inicio} a {data_fim} ({anos:.1f} anos)")
    print(f"Investimento Inicial: R$ {investimento_total_inicial:,.2f}")
    print(f"Carteira: R$ {valor_final_carteira:,.2f} | CAGR: {calculate_cagr(investimento_total_inicial, valor_final_carteira, anos):.2%}")
    if 'Selic' in curva_de_capital and not curva_de_capital['Selic'].isna().all():
        valor_final_selic = curva_de_capital['Selic'].iloc[-1]
        print(f"Selic:    R$ {valor_final_selic:,.2f} | CAGR: {calculate_cagr(investimento_total_inicial, valor_final_selic, anos):.2%}")
    if 'IMA-B' in curva_de_capital and not curva_de_capital['IMA-B'].isna().all():
        valor_final_imab = curva_de_capital['IMA-B'].iloc[-1]
        print(f"IMA-B 5+: R$ {valor_final_imab:,.2f} | CAGR: {calculate_cagr(investimento_total_inicial, valor_final_imab, anos):.2%}")

    return curva_de_capital

def run_monthly_contributions_backtest(data_historica, selic_diaria, imab_diario_ret, ipca_mensal, tickers_sa, data_inicio, data_fim):
    """Executa o backtest para o cenário de Aportes Mensais."""
    print("\n\n--- CENÁRIO 2: APORTES MENSAIS CORRIGIDOS PELO IPCA ---")
    all_dates = pd.date_range(start=data_inicio, end=data_fim, freq='D')
    valid_tickers = [col for col in tickers_sa if col in data_historica['Close'].columns and not data_historica['Close'][col].dropna().empty]
    columns_mensal = valid_tickers + ['Total', 'Selic', 'IMA-B', 'Total Investido', 'Aporte', 'Ativo Aportado']
    portfolio_mensal = pd.DataFrame(0.0, index=all_dates, columns=columns_mensal)
    portfolio_mensal['Ativo Aportado'] = ""
    num_shares = {ticker: 0.0 for ticker in valid_tickers}
    ipca_acumulado = (1 + ipca_mensal).cumprod().reindex(all_dates, method='ffill').fillna(1) if ipca_mensal is not None else pd.Series(1, index=all_dates)

    valor_selic = 0.0
    valor_imab = 0.0
    total_investido = 0.0
    last_month_processed = None

    print("Processando backtest com aportes mensais...")
    for dia in all_dates:
        if dia not in data_historica.index:
            if dia > all_dates[0]:
                portfolio_mensal.loc[dia, 'Total'] = portfolio_mensal.loc[:dia, 'Total'].iloc[-2] if len(portfolio_mensal.loc[:dia, 'Total']) > 1 else 0
                portfolio_mensal.loc[dia, 'Selic'] = valor_selic
                portfolio_mensal.loc[dia, 'IMA-B'] = valor_imab
                portfolio_mensal.loc[dia, 'Total Investido'] = total_investido
            continue

        current_month = (dia.year, dia.month)
        if current_month != last_month_processed:
            last_month_processed = current_month
            aporte_corrigido = config.APORTE_MENSAL_BASE * ipca_acumulado.loc[dia]
            total_investido += aporte_corrigido
            valor_selic += aporte_corrigido
            if imab_diario_ret is not None:
                valor_imab += aporte_corrigido

            portfolio_mensal.loc[dia, 'Aporte'] = aporte_corrigido

            valores_ativos = {ticker: num_shares[ticker] * data_historica.loc[dia, ('Close', ticker)] for ticker in valid_tickers if pd.notna(data_historica.loc[dia, ('Close', ticker)])}
            if valores_ativos:
                ativo_menor_valor = min(valores_ativos, key=valores_ativos.get)
                portfolio_mensal.loc[dia, 'Ativo Aportado'] = ativo_menor_valor
                preco = data_historica.loc[dia, ('Close', ativo_menor_valor)]
                if pd.notna(preco) and preco > 0:
                    num_shares[ativo_menor_valor] += aporte_corrigido / preco

        if selic_diaria is not None and dia in selic_diaria.index:
            valor_selic *= selic_diaria.loc[dia]
        if imab_diario_ret is not None and dia in imab_diario_ret.index:
            valor_imab *= (1 + imab_diario_ret.loc[dia])

        valor_total_dia = 0
        for ticker in valid_tickers:
            if pd.notna(data_historica.loc[dia, ('Close', ticker)]):
                preco_dia = data_historica.loc[dia, ('Close', ticker)]
                if ('Dividends', ticker) in data_historica.columns and pd.notna(data_historica.loc[dia, ('Dividends', ticker)]) and data_historica.loc[dia, ('Dividends', ticker)] > 0:
                    num_shares[ticker] += (num_shares[ticker] * data_historica.loc[dia, ('Dividends', ticker)]) / preco_dia
                valor_ativo = num_shares[ticker] * preco_dia
                portfolio_mensal.loc[dia, ticker] = valor_ativo
                valor_total_dia += valor_ativo

        portfolio_mensal.loc[dia, 'Total'] = valor_total_dia
        portfolio_mensal.loc[dia, 'Selic'] = valor_selic
        portfolio_mensal.loc[dia, 'IMA-B'] = valor_imab
        portfolio_mensal.loc[dia, 'Total Investido'] = total_investido

    portfolio_mensal.ffill(inplace=True)

    valor_final_carteira_m = portfolio_mensal['Total'].iloc[-1]
    total_investido_final = portfolio_mensal['Total Investido'].iloc[-1]
    anos = (pd.to_datetime(data_fim) - pd.to_datetime(data_inicio)).days / 365.25
    print("\n--- Resultados do Backtest (Aportes Mensais) ---")
    print(f"Período: {data_inicio} a {data_fim} ({anos:.1f} anos)")
    print(f"Total Investido (corrigido): R$ {total_investido_final:,.2f}")
    if total_investido_final > 0:
        print(f"Carteira: R$ {valor_final_carteira_m:,.2f} | Retorno sobre Investimento: {valor_final_carteira_m / total_investido_final - 1:.2%}")
        if 'Selic' in portfolio_mensal and not portfolio_mensal['Selic'].isna().all():
            valor_final_selic_m = portfolio_mensal['Selic'].iloc[-1]
            print(f"Selic:    R$ {valor_final_selic_m:,.2f} | Retorno sobre Investimento: {valor_final_selic_m / total_investido_final - 1:.2%}")
        if 'IMA-B' in portfolio_mensal and not portfolio_mensal['IMA-B'].isna().all():
            valor_final_imab_m = portfolio_mensal['IMA-B'].iloc[-1]
            print(f"IMA-B 5+: R$ {valor_final_imab_m:,.2f} | Retorno sobre Investimento: {valor_final_imab_m / total_investido_final - 1:.2%}")
    else:
        print(f"Carteira: R$ {valor_final_carteira_m:,.2f}")
        print("AVISO: Nenhum aporte foi processado.")

    return portfolio_mensal

def save_results_to_excel(lump_sum_results, monthly_results):
    """Salva os resultados dos backtests em arquivos Excel separados."""
    print("\nSalvando resultados em Excel...")
    try:
        with pd.ExcelWriter(config.ARQUIVO_RESULTADOS_APORTE_UNICO) as writer:
            lump_sum_results.resample('M').last().to_excel(writer, sheet_name='Aporte Unico (Mensal)')
        print(f"Resultados do Aporte Único salvos em '{config.ARQUIVO_RESULTADOS_APORTE_UNICO}'")

        with pd.ExcelWriter(config.ARQUIVO_RESULTADOS_APORTES_MENSAIS) as writer:
            monthly_results.resample('M').last().to_excel(writer, sheet_name='Aportes Mensais (Mensal)')
        print(f"Resultados dos Aportes Mensais salvos em '{config.ARQUIVO_RESULTADOS_APORTES_MENSAIS}'")
    except Exception as e:
        print(f"ERRO ao salvar resultados em Excel: {e}")

def plot_results(lump_sum_results, monthly_results):
    """Gera e exibe os gráficos dos resultados."""
    print("Gerando gráficos...")
    
    # Gráfico 1: Cenário de Aporte Único
    fig1, ax1 = plt.subplots(figsize=(14, 8))
    ax1.plot(lump_sum_results.index, lump_sum_results['Total'], label='Carteira', color='blue', linewidth=2)
    if 'Selic' in lump_sum_results and not lump_sum_results['Selic'].isna().all():
        ax1.plot(lump_sum_results.index, lump_sum_results['Selic'], label='Selic', color='green', linestyle='--')
    if 'IMA-B' in lump_sum_results and not lump_sum_results['IMA-B'].isna().all():
        ax1.plot(lump_sum_results.index, lump_sum_results['IMA-B'], label='IMA-B 5+', color='purple', linestyle='--')
    ax1.set_title('Cenário 1: Curva de Capital com Aporte Único', fontsize=18)
    ax1.set_xlabel('Data'); ax1.set_ylabel('Valor da Carteira (R$)'); ax1.legend(loc='upper left')
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))

    # Gráfico 2: Cenário de Aportes Mensais
    fig2, ax2 = plt.subplots(figsize=(14, 8))
    ax2.plot(monthly_results.index, monthly_results['Total'], label='Carteira', color='blue', linewidth=2)
    if 'Selic' in monthly_results and not monthly_results['Selic'].isna().all():
        ax2.plot(monthly_results.index, monthly_results['Selic'], label='Selic', color='green', linestyle='--')
    if 'IMA-B' in monthly_results and not monthly_results['IMA-B'].isna().all():
        ax2.plot(monthly_results.index, monthly_results['IMA-B'], label='IMA-B 5+', color='purple', linestyle='--')
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

def main():
    """Função principal que orquestra o processo de backtest."""
    warnings.simplefilter(action='ignore', category=FutureWarning)

    # Carrega configuração
    tickers_brutos = config.EMPRESAS_INPUT.split()
    tickers_sa = [config.TICKERS_MAP.get(t.upper()) for t in tickers_brutos]
    data_inicio = config.DATA_INICIO
    data_fim = config.DATA_FIM

    # --- Download de Todos os Dados ---
    print("--- INICIANDO DOWNLOAD DE DADOS ---")
    try:
        data_historica = yf.download(tickers_sa, start=data_inicio, end=data_fim, progress=True)
        if data_historica.empty:
            print("ERRO: Nenhum dado histórico de ações foi baixado. Verifique os tickers e o período.")
            return
    except Exception as e:
        print(f"ERRO CRÍTICO ao baixar dados do yfinance: {e}")
        return

    selic_df = download_bcb_series(432, 'selic', data_inicio, data_fim)
    ipca_df = download_bcb_series(433, 'ipca', data_inicio, data_fim)
    imab5_df = download_bcb_series(12467, 'imab5', data_inicio, data_fim)

    # --- Preparação dos Dados de Benchmark ---
    selic_diaria = (1 + selic_df['selic'] / 100) ** (1/252) if selic_df is not None else None
    ipca_mensal = ipca_df['ipca'] / 100 if ipca_df is not None else None

    if imab5_df is not None and not imab5_df.empty:
        imab_normalizado = imab5_df['imab5'] / imab5_df['imab5'].iloc[0]
        imab_diario_ret = imab_normalizado.pct_change().fillna(0)
        print("IMA-B 5+ carregado com sucesso.")
    else:
        print("AVISO: IMA-B 5+ não disponível. Benchmarks de renda fixa serão limitados à Selic.")
        imab_diario_ret = None

    # --- Execução dos Cenários de Backtest ---
    lump_sum_results = run_lump_sum_backtest(data_historica, selic_diaria, imab_diario_ret, tickers_sa, data_inicio, data_fim)
    monthly_results = run_monthly_contributions_backtest(data_historica, selic_diaria, imab_diario_ret, ipca_mensal, tickers_sa, data_inicio, data_fim)

    # --- Salvamento e Visualização ---
    if lump_sum_results is not None and monthly_results is not None:
        save_results_to_excel(lump_sum_results, monthly_results)
        plot_results(lump_sum_results, monthly_results)
    else:
        print("\nAVISO: Nenhum resultado foi gerado. Gráficos e salvamento em Excel foram ignorados.")

if __name__ == "__main__":
    main()

