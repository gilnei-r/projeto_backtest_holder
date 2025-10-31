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

def run_lump_sum_backtest(data_historica, benchmark_diaria, ipca_mensal, tickers_sa, data_inicio, data_fim):
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

    if benchmark_diaria is not None:
        benchmark_acumulada = benchmark_diaria.cumprod()
        curva_de_capital[config.BENCHMARK_NAME] = investimento_total_inicial * benchmark_acumulada.reindex(all_dates, method='ffill')

    curva_de_capital = calculate_ipca_benchmark(curva_de_capital, ipca_mensal, investimento_total_inicial)

    anos = (pd.to_datetime(data_fim) - pd.to_datetime(data_inicio)).days / 365.25
    valor_final_carteira = curva_de_capital['Total'].iloc[-1]
    print("\n--- Resultados do Backtest (Aporte Único) ---")
    print(f"Período: {data_inicio} a {data_fim} ({anos:.1f} anos)")
    print(f"Investimento Inicial: R$ {investimento_total_inicial:,.2f}")
    print(f"Carteira: R$ {valor_final_carteira:,.2f} | CAGR: {calculate_cagr(investimento_total_inicial, valor_final_carteira, anos):.2%}")
    if config.BENCHMARK_NAME in curva_de_capital and not curva_de_capital[config.BENCHMARK_NAME].isna().all():
        valor_final_benchmark = curva_de_capital[config.BENCHMARK_NAME].iloc[-1]
        print(f"{config.BENCHMARK_NAME}:    R$ {valor_final_benchmark:,.2f} | CAGR: {calculate_cagr(investimento_total_inicial, valor_final_benchmark, anos):.2%}")

    return curva_de_capital

def run_monthly_contributions_backtest(data_historica, benchmark_diaria, ipca_mensal, tickers_sa, data_inicio, data_fim):
    """Executa o backtest para o cenário de Aportes Mensais."""
    print("\n\n--- CENÁRIO 2: APORTES MENSAIS CORRIGIDOS PELO IPCA ---")
    if config.FREIO_ATIVO:
        print("Freio automático de aportes ATIVADO.")

    all_dates = pd.date_range(start=data_inicio, end=data_fim, freq='D')
    valid_tickers = [col for col in tickers_sa if col in data_historica.columns and not data_historica[col].dropna().empty]
    
    columns_to_initialize_zero = valid_tickers + ['Total', config.BENCHMARK_NAME, 'Total Investido']
    portfolio_mensal = pd.DataFrame(0.0, index=all_dates, columns=columns_to_initialize_zero)
    df_aportes = pd.DataFrame(0.0, index=all_dates, columns=valid_tickers)

    portfolio_mensal['Aporte'] = np.nan
    portfolio_mensal['Ativo Aportado'] = np.nan

    num_shares = {ticker: 0.0 for ticker in valid_tickers}
    ipca_acumulado = (1 + ipca_mensal).cumprod().reindex(all_dates, method='ffill').fillna(1) if ipca_mensal is not None else pd.Series(1, index=all_dates)

    aportes_recentes = {ticker: [] for ticker in valid_tickers}
    quarentena = {ticker: None for ticker in valid_tickers}
    quarentena_duracao = {ticker: config.FREIO_QUARENTENA_INICIAL for ticker in valid_tickers}

    valor_selic = 0.0
    total_investido = 0.0
    last_month_processed = None

    print("Processando backtest com aportes mensais...")
    for dia in all_dates:
        if dia not in data_historica.index:
            if dia > all_dates[0]:
                for ticker in valid_tickers:
                    portfolio_mensal.loc[dia, ticker] = portfolio_mensal.loc[dia - pd.Timedelta(days=1), ticker]
                portfolio_mensal.loc[dia, 'Total'] = portfolio_mensal.loc[dia - pd.Timedelta(days=1), 'Total']
                portfolio_mensal.loc[dia, config.BENCHMARK_NAME] = valor_selic
                portfolio_mensal.loc[dia, 'Total Investido'] = total_investido
            continue

        current_month = (dia.year, dia.month)
        if current_month != last_month_processed:
            last_month_processed = current_month
            aporte_corrigido = config.APORTE_MENSAL_BASE * ipca_acumulado.loc[dia]
            total_investido += aporte_corrigido
            valor_selic += aporte_corrigido

            portfolio_mensal.loc[dia, 'Aporte'] = aporte_corrigido

            ativos_elegiveis = valid_tickers
            if config.FREIO_ATIVO:
                for ticker in quarentena:
                    if quarentena[ticker] is not None and dia >= quarentena[ticker]:
                        quarentena[ticker] = None
                        print(f"  FREIO DESATIVADO para {ticker} em {dia.strftime('%Y-%m-%d')}.")

                ativos_elegiveis = [ticker for ticker in valid_tickers if quarentena[ticker] is None]
                if not ativos_elegiveis:
                    ativos_elegiveis = []

            valores_ativos = {ticker: num_shares[ticker] * data_historica.loc[dia, ticker] for ticker in ativos_elegiveis if pd.notna(data_historica.loc[dia, ticker])}

            if valores_ativos:
                ativos_ordenados = sorted(valores_ativos, key=valores_ativos.get)
                num_a_selecionar = config.NUMERO_EMPRESAS_POR_APORTE
                ativos_selecionados = ativos_ordenados[:num_a_selecionar]

                if ativos_selecionados:
                    aporte_por_ativo = aporte_corrigido / len(ativos_selecionados)
                    portfolio_mensal.loc[dia, 'Ativo Aportado'] = ",".join(ativos_selecionados)

                    for ticker in ativos_selecionados:
                        preco = data_historica.loc[dia, ticker]
                        if pd.notna(preco) and preco > 0:
                            num_shares[ticker] += aporte_por_ativo / preco
                            df_aportes.loc[dia, ticker] = aporte_por_ativo

                        if config.FREIO_ATIVO:
                            aportes_recentes[ticker].append(dia)
                            limite_tempo = dia - pd.DateOffset(months=config.FREIO_PERIODO_APORTES)
                            aportes_recentes[ticker] = [d for d in aportes_recentes[ticker] if d >= limite_tempo]

                            if len(aportes_recentes[ticker]) > 1:
                                print(f"  FREIO ATIVADO para {ticker} em {dia.strftime('%Y-%m-%d')}.")
                                fim_quarentena = dia + pd.DateOffset(months=quarentena_duracao[ticker])
                                quarentena[ticker] = fim_quarentena
                                print(f"  Ativo em quarentena até {fim_quarentena.strftime('%Y-%m-%d')}.")
                                quarentena_duracao[ticker] += config.FREIO_QUARENTENA_ADICIONAL
        
        if benchmark_diaria is not None and dia in benchmark_diaria.index:
            valor_selic *= benchmark_diaria.loc[dia]

        valor_total_dia = 0
        for ticker in valid_tickers:
            if pd.notna(data_historica.loc[dia, ticker]):
                preco_dia = data_historica.loc[dia, ticker]
                if 'Dividends' in data_historica.columns and pd.notna(data_historica.loc[dia, ('Dividends', ticker)]) and data_historica.loc[dia, ('Dividends', ticker)] > 0:
                    num_shares[ticker] += (num_shares[ticker] * data_historica.loc[dia, ('Dividends', ticker)]) / preco_dia
                valor_ativo = num_shares[ticker] * preco_dia
                portfolio_mensal.loc[dia, ticker] = valor_ativo
                valor_total_dia += valor_ativo

        portfolio_mensal.loc[dia, 'Total'] = valor_total_dia
        portfolio_mensal.loc[dia, config.BENCHMARK_NAME] = valor_selic
        portfolio_mensal.loc[dia, 'Total Investido'] = total_investido

    portfolio_mensal.ffill(inplace=True)
    df_aportes_acumulados = df_aportes.cumsum()

    portfolio_mensal = calculate_ipca_benchmark(portfolio_mensal, ipca_mensal, portfolio_mensal['Total Investido'])

    valor_final_carteira_m = portfolio_mensal['Total'].iloc[-1]
    total_investido_final = portfolio_mensal['Total Investido'].iloc[-1]
    anos = (pd.to_datetime(data_fim) - pd.to_datetime(data_inicio)).days / 365.25
    print("\n--- Resultados do Backtest (Aportes Mensais) ---")
    print(f"Período: {data_inicio} a {data_fim} ({anos:.1f} anos)")
    print(f"Total Investido (corrigido): R$ {total_investido_final:,.2f}")
    if total_investido_final > 0:
        print(f"Carteira: R$ {valor_final_carteira_m:,.2f} | Retorno sobre Investimento: {valor_final_carteira_m / total_investido_final - 1:.2%}")
        if config.BENCHMARK_NAME in portfolio_mensal and not portfolio_mensal[config.BENCHMARK_NAME].isna().all():
            valor_final_benchmark_m = portfolio_mensal[config.BENCHMARK_NAME].iloc[-1]
            print(f"{config.BENCHMARK_NAME}:    R$ {valor_final_benchmark_m:,.2f} | Retorno sobre Investimento: {valor_final_benchmark_m / total_investido_final - 1:.2%}")
    else:
        print(f"Carteira: R$ {valor_final_carteira_m:,.2f}")
        print("AVISO: Nenhum aporte foi processado.")

    return portfolio_mensal, df_aportes_acumulados

def calculate_ipca_benchmark(portfolio_df, ipca_mensal, initial_investment):
    """Calcula o benchmark IPCA + X% e o adiciona ao dataframe do portfólio."""
    if ipca_mensal is None:
        return portfolio_df

    # Converte a taxa de juros real anual para uma taxa diária
    taxa_juros_real_anual = config.IPCA_BENCHMARK_X / 100.0
    if taxa_juros_real_anual == 0:
        taxa_juros_real_diaria = 0.0
    else:
        taxa_juros_real_diaria = (1 + taxa_juros_real_anual) ** (1 / 252) - 1

    # Prepara o dataframe do benchmark
    benchmark_df = pd.DataFrame(index=portfolio_df.index)
    benchmark_df['ipca'] = ipca_mensal.reindex(benchmark_df.index, method='ffill')
    benchmark_df.fillna(0, inplace=True)

    # Identifica o último dia de cada mês no índice
    is_last_day_of_month = benchmark_df.index.to_series().dt.is_month_end

    # O fator de correção do IPCA é aplicado apenas no último dia do mês.
    ipca_fator = (1 + benchmark_df['ipca'] / 100).where(is_last_day_of_month, 1)

    # O juro real é aplicado diariamente.
    juro_real_fator = (1 + taxa_juros_real_diaria)

    # Combina os fatores
    fator_diario = ipca_fator * juro_real_fator
    
    # Calcula o benchmark acumulado
    benchmark_acumulado = fator_diario.cumprod()
    
    # Adiciona a coluna do benchmark ao dataframe do portfólio
    portfolio_df['IPCA_Benchmark'] = initial_investment * benchmark_acumulado
    
    return portfolio_df

def run_scenario_cdb_mixed(start_date, end_date, monthly_contribution, portfolio_data, benchmark_data, ipca_data, cdb_percentage):
    """Executa o backtest para o cenário com alocação em CDB."""
    print("\n\n--- CENÁRIO 3: APORTES MENSAIS COM ALOCAÇÃO EM CDB ---")

    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    valid_tickers = [col for col in config.TICKERS_EMPRESAS if col in portfolio_data.columns and not portfolio_data[col].dropna().empty]
    
    columns = valid_tickers + ['CDB', 'Total', config.BENCHMARK_NAME, 'Total Investido']
    results_df = pd.DataFrame(0.0, index=all_dates, columns=columns)
    df_aportes = pd.DataFrame(0.0, index=all_dates, columns=valid_tickers + ['CDB'])

    results_df['Aporte'] = np.nan
    results_df['Ativo Aportado'] = pd.NA

    num_shares = {ticker: 0.0 for ticker in valid_tickers}
    cdb_value = 0.0
    total_investido = 0.0
    valor_selic_benchmark = 0.0
    last_month_processed = None

    aportes_recentes = {ticker: [] for ticker in valid_tickers}
    quarentena = {ticker: None for ticker in valid_tickers}
    quarentena_duracao = {ticker: config.FREIO_QUARENTENA_INICIAL for ticker in valid_tickers}

    ipca_acumulado = (1 + ipca_data).cumprod().reindex(all_dates, method='ffill').fillna(1) if ipca_data is not None else pd.Series(1, index=all_dates)

    print("Processando backtest com aportes mensais e alocação em CDB...")
    for dia in all_dates:
        if benchmark_data is not None and dia in benchmark_data.index:
            cdb_value *= benchmark_data.loc[dia]
            valor_selic_benchmark *= benchmark_data.loc[dia]

        if dia not in portfolio_data.index:
            if dia > all_dates[0]:
                for ticker in valid_tickers:
                    results_df.loc[dia, ticker] = results_df.loc[dia - pd.Timedelta(days=1), ticker]
                results_df.loc[dia, 'CDB'] = cdb_value
                results_df.loc[dia, 'Total'] = results_df.loc[dia - pd.Timedelta(days=1), 'Total']
                results_df.loc[dia, config.BENCHMARK_NAME] = valor_selic_benchmark
                results_df.loc[dia, 'Total Investido'] = total_investido
            continue

        current_month = (dia.year, dia.month)
        if current_month != last_month_processed:
            last_month_processed = current_month
            aporte_corrigido = monthly_contribution * ipca_acumulado.loc[dia]
            total_investido += aporte_corrigido
            valor_selic_benchmark += aporte_corrigido
            results_df.loc[dia, 'Aporte'] = aporte_corrigido

            total_portfolio_value = sum(num_shares[ticker] * portfolio_data.loc[dia, ticker] for ticker in valid_tickers if pd.notna(portfolio_data.loc[dia, ticker])) + cdb_value

            if (total_portfolio_value > 0 and (cdb_value / total_portfolio_value) < cdb_percentage) or total_portfolio_value == 0:
                cdb_value += aporte_corrigido
                df_aportes.loc[dia, 'CDB'] = aporte_corrigido
                results_df.loc[dia, 'Ativo Aportado'] = 'CDB'
            else:
                valores_ativos = {ticker: num_shares[ticker] * portfolio_data.loc[dia, ticker] for ticker in valid_tickers if pd.notna(portfolio_data.loc[dia, ticker])}
                if valores_ativos:
                    ativo_menor_valor = min(valores_ativos, key=valores_ativos.get)
                    preco = portfolio_data.loc[dia, ativo_menor_valor]
                    if pd.notna(preco) and preco > 0:
                        num_shares[ativo_menor_valor] += aporte_corrigido / preco
                        df_aportes.loc[dia, ativo_menor_valor] = aporte_corrigido
                        results_df.loc[dia, 'Ativo Aportado'] = ativo_menor_valor

        valor_total_dia = 0
        for ticker in valid_tickers:
            if pd.notna(portfolio_data.loc[dia, ticker]):
                preco_dia = portfolio_data.loc[dia, ticker]
                if 'Dividends' in portfolio_data.columns and pd.notna(portfolio_data.loc[dia, ('Dividends', ticker)]) and portfolio_data.loc[dia, ('Dividends', ticker)] > 0:
                    num_shares[ticker] += (num_shares[ticker] * portfolio_data.loc[dia, ('Dividends', ticker)]) / preco_dia
                valor_ativo = num_shares[ticker] * preco_dia
                results_df.loc[dia, ticker] = valor_ativo
                valor_total_dia += valor_ativo
        
        results_df.loc[dia, 'CDB'] = cdb_value
        valor_total_dia += cdb_value
        results_df.loc[dia, 'Total'] = valor_total_dia
        results_df.loc[dia, config.BENCHMARK_NAME] = valor_selic_benchmark
        results_df.loc[dia, 'Total Investido'] = total_investido

    numeric_cols = valid_tickers + ['CDB', 'Total', config.BENCHMARK_NAME, 'Total Investido']
    results_df[numeric_cols] = results_df[numeric_cols].ffill()
    df_aportes_acumulados = df_aportes.cumsum()

    results_df = calculate_ipca_benchmark(results_df, ipca_data, results_df['Total Investido'])
    
    valor_final_carteira = results_df['Total'].iloc[-1]
    total_investido_final = results_df['Total Investido'].iloc[-1]
    anos = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days / 365.25
    print("\n--- Resultados do Backtest (Aportes Mensais com CDB) ---")
    print(f"Período: {start_date} a {end_date} ({anos:.1f} anos)")
    print(f"Total Investido (corrigido): R$ {total_investido_final:,.2f}")
    if total_investido_final > 0:
        print(f"Carteira: R$ {valor_final_carteira:,.2f} | Retorno sobre Investimento: {valor_final_carteira / total_investido_final - 1:.2%}")
        if config.BENCHMARK_NAME in results_df and not results_df[config.BENCHMARK_NAME].isna().all():
            valor_final_benchmark_m = results_df[config.BENCHMARK_NAME].iloc[-1]
            print(f"{config.BENCHMARK_NAME} (Benchmark): R$ {valor_final_benchmark_m:,.2f} | Retorno sobre Investimento: {valor_final_benchmark_m / total_investido_final - 1:.2%}")
    else:
        print(f"Carteira: R$ {valor_final_carteira:,.2f}")

    return results_df, df_aportes_acumulados