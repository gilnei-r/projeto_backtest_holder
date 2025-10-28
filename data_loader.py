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
    """Busca os dados do IPCA usando o código da série do BCB."""
    return download_bcb_series(IPCA_SERIES_CODE, 'ipca', start_date, end_date)

def get_selic_data(start_date, end_date):
    """Busca os dados da SELIC usando o código da série do BCB."""
    return download_bcb_series(SELIC_SERIES_CODE, 'selic', start_date, end_date)

def download_stock_data(tickers, start_date, end_date):
    """Baixa dados históricos de ações, com cache para evitar downloads desnecessários."""
    print("--- VERIFICANDO DADOS DE AÇÕES ---")
    
    use_cache = False
    if os.path.exists(STOCK_DATA_FILE):
        last_modified_time = os.path.getmtime(STOCK_DATA_FILE)
        if (datetime.now() - datetime.fromtimestamp(last_modified_time)).days < DATA_UPDATE_DAYS:
            print(f"Usando dados de cache do arquivo '{STOCK_DATA_FILE}' (menos de {DATA_UPDATE_DAYS} dia(s) de idade).")
            use_cache = True

    if use_cache:
        data_historica = pd.read_csv(STOCK_DATA_FILE, header=[0, 1], index_col=0, parse_dates=True)
    else:
        print("Baixando novos dados de ações...")
        try:
            data_historica = yf.download(tickers, start=start_date, end=end_date, progress=True)
            if data_historica.empty:
                print("ERRO: Nenhum dado histórico de ações foi baixado.")
                return None
            # Salva os dados baixados em cache
            data_historica.to_csv(STOCK_DATA_FILE)
            print(f"Novos dados salvos em '{STOCK_DATA_FILE}'.")
        except Exception as e:
            print(f"ERRO CRÍTICO ao baixar dados do yfinance: {e}")
            return None

    # Garante que o preenchimento de dados ausentes seja sempre executado
    data_historica.ffill(inplace=True)
    print("Dados de ações carregados e processados.")
    return data_historica

def prepare_benchmark_data(selic_df, ipca_df):
    """Prepara os dados de benchmark (Selic e IPCA)."""
    selic_diaria = (1 + selic_df['selic'] / 100) ** (1/252) if selic_df is not None else None
    ipca_mensal = ipca_df['ipca'] / 100 if ipca_df is not None else None
    return selic_diaria, ipca_mensal
