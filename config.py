# -*- coding: utf-8 -*-

"""
CONFIGURAÇÃO DO BACKTEST

Este arquivo centraliza todas as variáveis de configuração para o script de backtest.
Modifique os valores aqui para alterar os parâmetros da simulação sem alterar o
código principal.
"""

from datetime import datetime

# --- Configuração Geral ---

# Lista de tickers de ações a serem analisadas.
# Os tickers devem ser separados por espaços. Ex: "ITUB4 BBDC4 BBAS3"
EMPRESAS_INPUT = "ITUB BBDC BBAS ABEV ITSA VIVT BRFS CRUZ UGPA PCAR GGBR WEGE PSSA BRSR CYRE GOAU WHRL NATU GRND EMBR GUAR COCE TRPL AMER RADL ALPA BAZA LEVE POMO RAPT ETER FRAS CGRA"

# Mapeamento de tickers curtos para os tickers completos com sufixo ".SA"
# usado pelo yfinance.
TICKERS_MAP = {
    'ITUB': 'ITUB4.SA', 'BBDC': 'BBDC4.SA', 'BBAS': 'BBAS3.SA', 'ABEV': 'ABEV3.SA',
    'ITSA': 'ITSA4.SA', 'VIVT': 'VIVT3.SA', 'BRFS': 'BRFS3.SA', 'CRUZ': 'CRUZ3.SA',
    'UGPA': 'UGPA3.SA', 'PCAR': 'PCAR3.SA', 'GGBR': 'GGBR4.SA', 'WEGE': 'WEGE3.SA',
    'PSSA': 'PSSA3.SA', 'BRSR': 'BRSR6.SA', 'CYRE': 'CYRE3.SA', 'GOAU': 'GOAU4.SA',
    'WHRL': 'WHRL4.SA', 'NATU': 'NATU3.SA', 'GRND': 'GRND3.SA', 'EMBR': 'EMBR3.SA',
    'GUAR': 'GUAR3.SA', 'COCE': 'COCE5.SA', 'TRPL': 'TRPL4.SA', 'AMER': 'AMER3.SA',
    'RADL': 'RADL3.SA', 'ALPA': 'ALPA4.SA', 'BAZA': 'BAZA3.SA', 'LEVE': 'LEVE3.SA',
    'POMO': 'POMO4.SA', 'RAPT': 'RAPT4.SA', 'ETER': 'ETER3.SA', 'FRAS': 'FRAS3.SA',
    'CGRA': 'CGRA4.SA'
}

# Data de início do backtest no formato "AAAA-MM-DD".
DATA_INICIO = "2015-01-01"

# Data de fim do backtest. Por padrão, usa a data de hoje.
DATA_FIM = datetime.today().strftime('%Y-%m-%d')


# --- Configuração do Cenário 1: Aporte Único ---

# Valor a ser investido em cada empresa no início da simulação.
# O investimento total será (VALOR_INVESTIDO_POR_EMPRESA * número de empresas).
VALOR_INVESTIDO_POR_EMPRESA = 1000.00


# --- Configuração do Cenário 2: Aportes Mensais ---

# Valor base do aporte mensal.
# Este valor será corrigido mensalmente pela inflação (IPCA).
APORTE_MENSAL_BASE = 1000.0


# --- Configuração de Saída ---

# Nomes dos arquivos de saída para os resultados em Excel.
ARQUIVO_RESULTADOS_APORTE_UNICO = "backtest_results_lump_sum.xlsx"
ARQUIVO_RESULTADOS_APORTES_MENSAIS = "backtest_results_monthly.xlsx"
