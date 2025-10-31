# -*- coding: utf-8 -*-

import os
import time
import pandas as pd
import yfinance as yf
from bcb import sgs
from datetime import datetime, timedelta
import MetaTrader5 as mt5
import config
from config import DATA_UPDATE_DAYS, BENCHMARK_SERIES_CODE, BENCHMARK_NAME

# --- Constantes de Arquivos e Séries ---
STOCK_DATA_FILE = "stock_data.csv"
IPCA_SERIES_CODE = 433

def _is_cache_valid(file_path):
    """Verifica se um arquivo de cache é válido com base na data de modificação."""
    if not os.path.exists(file_path):
        return False
    last_modified_time = os.path.getmtime(file_path)
    if (datetime.now() - datetime.fromtimestamp(last_modified_time)).days < DATA_UPDATE_DAYS:
        return True
    return False

def connect_mt5():
    """Conecta ao terminal MetaTrader 5."""
    for i in range(config.MT5_RETRIES):
        if mt5.initialize():
            print("Conectado ao MetaTrader 5.")
            return True
        else:
            print(f"Falha ao conectar ao MetaTrader 5, tentativa {i+1}/{config.MT5_RETRIES}.")
            time.sleep(config.MT5_TIMEOUT)
    print("Não foi possível conectar ao MetaTrader 5.")
    return False

def download_mt5_data(ticker, start_date, end_date):
    """Baixa dados históricos do MetaTrader 5."""
    if not connect_mt5():
        return None

    rates = mt5.copy_rates_from_pos(ticker, mt5.TIMEFRAME_D1, 0, 99999)
    mt5.shutdown()

    if rates is None:
        print(f"Nenhum dado encontrado para {ticker} no MetaTrader 5.")
        return None

    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    df.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'tick_volume': 'Volume'}, inplace=True)
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    
    # O MT5 não fornece dados de dividendos, então criamos uma coluna de zeros.
    df['Dividends'] = 0.0
    
    return df

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

def get_benchmark_data(start_date, end_date):
    """Busca os dados do benchmark (CDI ou SELIC), com cache em arquivo CSV."""
    os.makedirs('data', exist_ok=True)
    file_path = f'data/{BENCHMARK_NAME}.csv'

    if _is_cache_valid(file_path):
        print(f"Usando cache para {BENCHMARK_NAME} de '{file_path}'.")
        return pd.read_csv(file_path, index_col=0, parse_dates=True)

    print(f"Baixando novos dados para {BENCHMARK_NAME}...")
    benchmark_df = download_bcb_series(BENCHMARK_SERIES_CODE, BENCHMARK_NAME.lower(), start_date, end_date)
    if benchmark_df is not None and not benchmark_df.empty:
        benchmark_df.to_csv(file_path)
        print(f"Novos dados de {BENCHMARK_NAME} salvos em '{file_path}'.")
    return benchmark_df

def _load_from_yfinance(tickers, start_date, end_date):
    """Baixa dados do yfinance."""
    all_data = {}
    failed_tickers = []

    for ticker in tickers:
        file_path = f"data/{ticker}.csv"
        ticker_data = None

        if _is_cache_valid(file_path):
            print(f"Usando cache para {ticker} de '{file_path}'.")
            ticker_data = pd.read_csv(file_path, header=0, index_col=0, parse_dates=True)
        else:
            print(f"Baixando novos dados para {ticker} via yfinance...")
            try:
                ticker_data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True, progress=False)
                if ticker_data.empty:
                    print(f"AVISO: Nenhum dado baixado para {ticker} via yfinance.")
                    ticker_data = None
                else:
                    ticker_data.to_csv(file_path)
                    print(f"Novos dados para {ticker} salvos em '{file_path}'.")
            except Exception as e:
                print(f"ERRO ao baixar dados para {ticker} via yfinance: {e}")
                ticker_data = None

        if ticker_data is not None:
            all_data[ticker] = ticker_data['Adj Close']
        else:
            failed_tickers.append(ticker)

    return all_data, failed_tickers

def _load_from_metastock(tickers, path):
    """Carrega dados de arquivos CSV locais (formato Metastock)."""
    if not os.path.isdir(path):
        raise FileNotFoundError(f"O caminho para o Metastock não foi encontrado: {path}")

    all_data = {}
    failed_tickers = []

    for ticker in tickers:
        # Remove o sufixo .SA para corresponder aos nomes de arquivo locais
        local_ticker = ticker.replace('.SA', '')
        file_path = os.path.join(path, f"{local_ticker}.csv")

        if not os.path.exists(file_path):
            print(f"AVISO: Arquivo não encontrado para {ticker} em {file_path}. Pulando.")
            failed_tickers.append(ticker)
            continue

        try:
            print(f"Carregando dados para {ticker} de '{file_path}'.")
            ticker_data = pd.read_csv(file_path, index_col='Date', parse_dates=True)
            
            if 'Adj Close' not in ticker_data.columns:
                 print(f"AVISO: Coluna 'Adj Close' não encontrada em {file_path} para {ticker}. Pulando.")
                 failed_tickers.append(ticker)
                 continue

            all_data[ticker] = ticker_data['Adj Close']
        except Exception as e:
            print(f"ERRO ao carregar dados para {ticker} de {file_path}: {e}")
            failed_tickers.append(ticker)

    return all_data, failed_tickers

def _load_from_mt5(tickers, start_date, end_date):
    """Baixa dados exclusivamente do MetaTrader 5."""
    all_data = {}
    failed_tickers = []

    if not connect_mt5():
        return {}, tickers

    for ticker in tickers:
        mt5_ticker = ticker.replace('.SA', '')
        print(f"Baixando {mt5_ticker} via MetaTrader 5...")
        ticker_data = download_mt5_data(mt5_ticker, start_date, end_date)

        if ticker_data is not None and not ticker_data.empty:
            # O MT5 não fornece 'Adj Close', usamos 'Close'
            all_data[ticker] = ticker_data['Close']
        else:
            failed_tickers.append(ticker)
    
    mt5.shutdown()
    return all_data, failed_tickers

def download_stock_data(tickers, start_date, end_date):
    """
    Baixa ou carrega dados históricos de ações de diferentes fontes,
    com cache para cada ticker individualmente.
    """
    print("--- VERIFICANDO DADOS DE AÇÕES ---")
    os.makedirs('data', exist_ok=True)

    all_data = {}
    failed_tickers = []

    if config.DATA_SOURCE == 'yahoofinance':
        all_data, failed_tickers = _load_from_yfinance(tickers, start_date, end_date)
    elif config.DATA_SOURCE == 'metatrader5':
        all_data, failed_tickers = _load_from_mt5(tickers, start_date, end_date)
    elif config.DATA_SOURCE == 'metastock':
        all_data, failed_tickers = _load_from_metastock(tickers, config.METASTOCK_PATH)
    else:
        raise ValueError(f"Fonte de dados desconhecida: {config.DATA_SOURCE}")

    if not all_data:
        print("ERRO CRÍTICO: Falha ao carregar dados para todos os tickers.")
        return None, failed_tickers

    master_df = pd.concat(all_data.values(), axis=1, keys=all_data.keys())
    master_df.columns.name = 'Ticker'
    master_df.ffill(inplace=True)

    print("Dados de ações carregados e processados.")
    return master_df, failed_tickers

def prepare_benchmark_data(benchmark_df, ipca_df):
    """Prepara os dados de benchmark (CDI/Selic e IPCA)."""
    benchmark_diaria = (1 + benchmark_df[BENCHMARK_NAME.lower()] / 100)
    ipca_mensal = ipca_df['ipca'] / 100 if ipca_df is not None else None
    return benchmark_diaria, ipca_mensal