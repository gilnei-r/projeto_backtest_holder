# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import config

# --- Funções Auxiliares ---

def calculate_cagr(start_value, end_value, years):
    """Calcula a Taxa de Crescimento Anual Composta (CAGR)."""
    if start_value == 0 or years <= 0:
        return 0
    return (end_value / start_value) ** (1 / years) - 1

def run_lump_sum_backtest(data_historica, selic_diaria, tickers_sa, data_inicio, data_fim):
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

    anos = (pd.to_datetime(data_fim) - pd.to_datetime(data_inicio)).days / 365.25
    valor_final_carteira = curva_de_capital['Total'].iloc[-1]
    print("\n--- Resultados do Backtest (Aporte Único) ---")
    print(f"Período: {data_inicio} a {data_fim} ({anos:.1f} anos)")
    print(f"Investimento Inicial: R$ {investimento_total_inicial:,.2f}")
    print(f"Carteira: R$ {valor_final_carteira:,.2f} | CAGR: {calculate_cagr(investimento_total_inicial, valor_final_carteira, anos):.2%}")
    if 'Selic' in curva_de_capital and not curva_de_capital['Selic'].isna().all():
        valor_final_selic = curva_de_capital['Selic'].iloc[-1]
        print(f"Selic:    R$ {valor_final_selic:,.2f} | CAGR: {calculate_cagr(investimento_total_inicial, valor_final_selic, anos):.2%}")

    return curva_de_capital

def run_monthly_contributions_backtest(data_historica, selic_diaria, ipca_mensal, tickers_sa, data_inicio, data_fim):
    """Executa o backtest para o cenário de Aportes Mensais."""
    print("\n\n--- CENÁRIO 2: APORTES MENSAIS CORRIGIDOS PELO IPCA ---")
    if config.FREIO_ATIVO:
        print("Freio automático de aportes ATIVADO.")

    all_dates = pd.date_range(start=data_inicio, end=data_fim, freq='D')
    valid_tickers = [col for col in tickers_sa if col in data_historica['Close'].columns and not data_historica['Close'][col].dropna().empty]
    
    # Correção: Inicia colunas 'Aporte' e 'Ativo Aportado' com NaN para permitir o preenchimento (ffill)
    columns_to_initialize_zero = valid_tickers + ['Total', 'Selic', 'Total Investido']
    portfolio_mensal = pd.DataFrame(0.0, index=all_dates, columns=columns_to_initialize_zero)
    portfolio_mensal['Aporte'] = np.nan
    portfolio_mensal['Ativo Aportado'] = np.nan

    num_shares = {ticker: 0.0 for ticker in valid_tickers}
    ipca_acumulado = (1 + ipca_mensal).cumprod().reindex(all_dates, method='ffill').fillna(1) if ipca_mensal is not None else pd.Series(1, index=all_dates)

    # --- Variáveis para o Freio Automático ---
    aportes_recentes = {ticker: [] for ticker in valid_tickers}
    quarentena = {ticker: None for ticker in valid_tickers}
    quarentena_duracao = {ticker: config.FREIO_QUARENTENA_INICIAL for ticker in valid_tickers}
    # -----------------------------------------

    valor_selic = 0.0
    total_investido = 0.0
    last_month_processed = None

    print("Processando backtest com aportes mensais...")
    for dia in all_dates:
        if dia not in data_historica.index:
            if dia > all_dates[0]:
                # Forward-fill: propaga valores do dia anterior para dias sem negociação
                for ticker in valid_tickers:
                    portfolio_mensal.loc[dia, ticker] = portfolio_mensal.loc[:dia, ticker].iloc[-2] if len(portfolio_mensal.loc[:dia, ticker]) > 1 else 0
                portfolio_mensal.loc[dia, 'Total'] = portfolio_mensal.loc[:dia, 'Total'].iloc[-2] if len(portfolio_mensal.loc[:dia, 'Total']) > 1 else 0
                portfolio_mensal.loc[dia, 'Selic'] = valor_selic
                portfolio_mensal.loc[dia, 'Total Investido'] = total_investido
            continue

        current_month = (dia.year, dia.month)
        if current_month != last_month_processed:
            last_month_processed = current_month
            aporte_corrigido = config.APORTE_MENSAL_BASE * ipca_acumulado.loc[dia]
            total_investido += aporte_corrigido
            valor_selic += aporte_corrigido

            portfolio_mensal.loc[dia, 'Aporte'] = aporte_corrigido

            # --- Lógica do Freio Automático ---
            ativos_elegiveis = valid_tickers
            if config.FREIO_ATIVO:
                # Libera ativos da quarentena se a data já passou
                for ticker in quarentena:
                    if quarentena[ticker] is not None and dia >= quarentena[ticker]:
                        quarentena[ticker] = None
                        print(f"  FREIO DESATIVADO para {ticker} em {dia.strftime('%Y-%m-%d')}.")

                ativos_elegiveis = [
                    ticker for ticker in valid_tickers if quarentena[ticker] is None
                ]
                # Se todos estiverem em quarentena, não aporta em ninguém.
                if not ativos_elegiveis:
                    ativos_elegiveis = []


            valores_ativos = {
                ticker: num_shares[ticker] * data_historica.loc[dia, ('Close', ticker)]
                for ticker in ativos_elegiveis
                if pd.notna(data_historica.loc[dia, ('Close', ticker)])
            }
            # ------------------------------------

            if valores_ativos:
                # --- Lógica de Seleção e Aporte Dividido ---
                
                # Ordena os ativos elegíveis pelo seu valor total em carteira (do menor para o maior)
                ativos_ordenados = sorted(valores_ativos, key=valores_ativos.get)
                
                # Seleciona os 'n' primeiros, ou menos se não houver 'n' ativos elegíveis
                num_a_selecionar = config.NUMERO_EMPRESAS_POR_APORTE
                ativos_selecionados = ativos_ordenados[:num_a_selecionar]

                if ativos_selecionados:
                    # Divide o aporte igualmente entre os ativos selecionados
                    aporte_por_ativo = aporte_corrigido / len(ativos_selecionados)
                    
                    # Registra os tickers que receberão aporte
                    portfolio_mensal.loc[dia, 'Ativo Aportado'] = ",".join(ativos_selecionados)

                    # Itera sobre os ativos selecionados para fazer o aporte e aplicar o freio
                    for ticker in ativos_selecionados:
                        preco = data_historica.loc[dia, ('Close', ticker)]
                        if pd.notna(preco) and preco > 0:
                            num_shares[ticker] += aporte_por_ativo / preco

                        # --- Lógica de Gatilho do Freio (aplicada individualmente) ---
                        if config.FREIO_ATIVO:
                            aportes_recentes[ticker].append(dia)
                            
                            # Remove aportes mais antigos que o período de verificação
                            limite_tempo = dia - pd.DateOffset(months=config.FREIO_PERIODO_APORTES)
                            aportes_recentes[ticker] = [
                                d for d in aportes_recentes[ticker] if d >= limite_tempo
                            ]

                            if len(aportes_recentes[ticker]) > 1:
                                print(f"  FREIO ATIVADO para {ticker} em {dia.strftime('%Y-%m-%d')}.")
                                
                                # Define a data de fim da quarentena
                                fim_quarentena = dia + pd.DateOffset(months=quarentena_duracao[ticker])
                                quarentena[ticker] = fim_quarentena
                                print(f"  Ativo em quarentena até {fim_quarentena.strftime('%Y-%m-%d')}.")

                                # Aumenta a próxima duração da quarentena para este ativo
                                quarentena_duracao[ticker] += config.FREIO_QUARENTENA_ADICIONAL
        
        if selic_diaria is not None and dia in selic_diaria.index:
            valor_selic *= selic_diaria.loc[dia]

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
    else:
        print(f"Carteira: R$ {valor_final_carteira_m:,.2f}")
        print("AVISO: Nenhum aporte foi processado.")

    return portfolio_mensal
