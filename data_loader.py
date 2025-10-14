# -*- coding: utf-8 -*-

import time
import pandas as pd
import yfinance as yf
from bcb import sgs

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

def download_stock_data(tickers, start_date, end_date):
    """Baixa dados históricos de ações e preenche valores ausentes."""
    print("--- INICIANDO DOWNLOAD DE DADOS DE AÇÕES ---")
    try:
        data_historica = yf.download(tickers, start=start_date, end=end_date, progress=True)
        if data_historica.empty:
            print("ERRO: Nenhum dado histórico de ações foi baixado. Verifique os tickers e o período.")
            return None

        # Correção: Preenche dados de preço ausentes para garantir a continuidade da simulação
        data_historica.ffill(inplace=True)
        return data_historica
    except Exception as e:
        print(f"ERRO CRÍTICO ao baixar dados do yfinance: {e}")
        return None

def prepare_benchmark_data(selic_df, ipca_df):
    """Prepara os dados de benchmark (Selic e IPCA)."""
    selic_diaria = (1 + selic_df['selic'] / 100) ** (1/252) if selic_df is not None else None
    ipca_mensal = ipca_df['ipca'] / 100 if ipca_df is not None else None
    return selic_diaria, ipca_mensal
