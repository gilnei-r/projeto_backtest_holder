# -*- coding: utf-8 -*-

import os
import time
import pandas as pd
import yfinance as yf
from bcb import sgs
from datetime import datetime, timedelta
from config import DATA_UPDATE_DAYS

# --- Constantes de Arquivos e Séries ---
STOCK_DATA_FILE = "stock_data.csv"
IPCA_SERIES_CODE = 433
SELIC_SERIES_CODE = 432

def _is_cache_valid(file_path):
    """Verifica se um arquivo de cache é válido com base na data de modificação."""
    if not os.path.exists(file_path):
        return False
    last_modified_time = os.path.getmtime(file_path)
    if (datetime.now() - datetime.fromtimestamp(last_modified_time)).days < DATA_UPDATE_DAYS:
        return True
    return False

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

def get_ipca_data(start_date, end_date):
    """Busca os dados do IPCA, com cache em arquivo CSV."""
    os.makedirs('data', exist_ok=True)
    file_path = 'data/IPCA.csv'
    
    if _is_cache_valid(file_path):
        print(f"Usando cache para IPCA de '{file_path}'.")
        return pd.read_csv(file_path, index_col=0, parse_dates=True)
    
    print("Baixando novos dados para IPCA...")
    ipca_df = download_bcb_series(IPCA_SERIES_CODE, 'ipca', start_date, end_date)
    if ipca_df is not None and not ipca_df.empty:
        ipca_df.to_csv(file_path)
        print(f"Novos dados de IPCA salvos em '{file_path}'.")
    return ipca_df

def get_selic_data(start_date, end_date):
    """Busca os dados da SELIC, com cache em arquivo CSV."""
    os.makedirs('data', exist_ok=True)
    file_path = 'data/SELIC.csv'

    if _is_cache_valid(file_path):
        print(f"Usando cache para SELIC de '{file_path}'.")
        return pd.read_csv(file_path, index_col=0, parse_dates=True)

    print("Baixando novos dados para SELIC...")
    selic_df = download_bcb_series(SELIC_SERIES_CODE, 'selic', start_date, end_date)
    if selic_df is not None and not selic_df.empty:
        selic_df.to_csv(file_path)
        print(f"Novos dados de SELIC salvos em '{file_path}'.")
    return selic_df

def download_stock_data(tickers, start_date, end_date):
    """Baixa dados históricos de ações, com cache para cada ticker individualmente."""
    print("--- VERIFICANDO DADOS DE AÇÕES ---")
    os.makedirs('data', exist_ok=True)
    
    all_data = {}

    for ticker in tickers:
        file_path = f"data/{ticker}.csv"

        if _is_cache_valid(file_path):
            print(f"Usando cache para {ticker} de '{file_path}'.")
            # Lê CSV com header multi-nível do yfinance
            ticker_data = pd.read_csv(file_path, header=[0, 1], index_col=0, parse_dates=True)
            # Remove o nível do ticker das colunas (segunda linha do header)
            ticker_data.columns = ticker_data.columns.droplevel(1)
        else:
            print(f"Baixando novos dados para {ticker}...")
            try:
                ticker_data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True, progress=False, multi_level_index=False)
                if ticker_data.empty:
                    print(f"AVISO: Nenhum dado baixado para {ticker}. Pode ser um ticker inválido ou sem dados no período.")
                    continue
                ticker_data.to_csv(file_path)
                print(f"Novos dados para {ticker} salvos em '{file_path}'.")
            except Exception as e:
                print(f"ERRO ao baixar dados para {ticker}: {e}")
                continue

        all_data[ticker] = ticker_data

    if not all_data:
        print("ERRO CRÍTICO: Falha ao carregar dados para todos os tickers.")
        return None

    # Combina os dados de todos os tickers em um único DataFrame com colunas MultiIndex
    data_historica = pd.concat(all_data.values(), keys=all_data.keys(), axis=1)

    # Inverte os níveis do MultiIndex para ter (metric, ticker) ao invés de (ticker, metric)
    data_historica.columns = data_historica.columns.swaplevel(0, 1)
    data_historica.sort_index(axis=1, inplace=True)

    # Garante que o preenchimento de dados ausentes seja sempre executado
    data_historica.ffill(inplace=True)
    print("Dados de ações carregados e processados.")
    return data_historica

def prepare_benchmark_data(selic_df, ipca_df):
    """Prepara os dados de benchmark (Selic e IPCA)."""
    selic_diaria = (1 + selic_df['selic'] / 100) ** (1/252) if selic_df is not None else None
    ipca_mensal = ipca_df['ipca'] / 100 if ipca_df is not None else None
    return selic_diaria, ipca_mensal
