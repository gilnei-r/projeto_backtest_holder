# -*- coding: utf-8 -*-

"""
CONFIGURAÇÃO DO BACKTEST

Este arquivo centraliza todas as variáveis de configuração para o script de backtest.
Modifique os valores aqui para alterar os parâmetros da simulação sem alterar o
código principal.
"""

from datetime import datetime

# --- Configuração Geral ---

# Lista de tickers de ações a serem analisadas, no formato requerido pelo yfinance (com sufixo .SA).
'''
TICKERS_EMPRESAS = [
    'ITUB4.SA', 'BBDC4.SA', 'BBAS3.SA', 'ABEV3.SA', 'ITSA4.SA', 'VIVT3.SA', 
    'BRFS3.SA', 'CRUZ3.SA', 'UGPA3.SA', 'PCAR3.SA', 'GGBR4.SA', 'WEGE3.SA', 
    'PSSA3.SA', 'BRSR6.SA', 'CYRE3.SA', 'GOAU4.SA', 'WHRL4.SA', 'NATU3.SA', 
    'GRND3.SA', 'EMBR3.SA', 'GUAR3.SA', 'COCE5.SA', 'TRPL4.SA', 'AMER3.SA', 
    'RADL3.SA', 'ALPA4.SA', 'BAZA3.SA', 'LEVE3.SA', 'POMO4.SA', 'RAPT4.SA', 
    'ETER3.SA', 'FRAS3.SA', 'CGRA4.SA'
]
'''
'''
TICKERS_EMPRESAS = [
    'ABEV3.SA', 'B3SA3.SA', 'BBSE3.SA', 'CIEL3.SA', 'COGN3.SA', 'EGIE3.SA',
    'EZTC3.SA', 'FLRY3.SA', 'GRND3.SA', 'HYPE3.SA', 'ITUB3.SA', 'WEGE3.SA',
    'LREN3.SA', 'MDIA3.SA', 'ODPV3.SA', 'PSSA3.SA', 'QUAL3.SA', 'RADL3.SA',
    'TOTS3.SA', 'UGPA3.SA'
]
'''
TICKERS_EMPRESAS = [
    'ABEV3.SA', 'AZZA3.SA', 'BBAS3.SA', 'BBDC3.SA', 'BBSE3.SA', 'BRFS3.SA',
    'B3SA3.SA', 'CCRO3.SA', 'CGRA3.SA', 'CIEL3.SA', 'CMIG3.SA', 'CVCB3.SA',
    'EGIE3.SA', 'ENBR3.SA', 'EQTL3.SA', 'ESTC3.SA', 'EZTC3.SA', 'FLRY3.SA',
    'GRND3.SA', 'HGTX3.SA', 'HYPE3.SA', 'IRBR3.SA', 'ITSA3.SA', 'ITUB3.SA',
    'COGN3.SA', 'LEVE3.SA', 'LINX3.SA', 'LREN3.SA', 'MDIA3.SA', 'MPLU3.SA',
    'MULT3.SA', 'NATU3.SA', 'ODPV3.SA', 'PETR3.SA', 'PSSA3.SA', 'PTBL3.SA',
    'QUAL3.SA', 'RADL3.SA', 'RENT3.SA', 'SAPR3.SA', 'SBSP3.SA', 'SEER3.SA',
    'SNSL3.SA', 'TAEE3.SA', 'TIET3.SA', 'TOTS3.SA', 'UGPA3.SA', 'VALE3.SA',
    'VLID3.SA', 'WEGE3.SA', 'WIZC3.SA'
]

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

# Número de empresas em que o aporte mensal será dividido.
# O valor será dividido igualmente entre as 'n' empresas de menor valor na carteira.
# Se for 1, o comportamento é o original (aporta tudo na empresa de menor valor).
NUMERO_EMPRESAS_POR_APORTE = 2/


# --- Configuração de Saída ---

# Nomes dos arquivos de saída para os resultados em Excel.
ARQUIVO_RESULTADOS_APORTE_UNICO = "backtest_results_lump_sum.xlsx"
ARQUIVO_RESULTADOS_APORTES_MENSAIS = "backtest_results_monthly.xlsx"


# --- Configuração do Freio Automático (Cenário 2) ---

# Ativa ou desativa o freio automático de aportes.
# Se True, impede aportes consecutivos no mesmo ativo.
FREIO_ATIVO = True

# Período (em meses) para verificar aportes repetidos no mesmo ativo.
# Ex: 2 significa que se houver mais de 1 aporte no mesmo ativo em 2 meses, o freio é ativado.
FREIO_PERIODO_APORTES = 3

# Duração inicial da quarentena (em meses) para um ativo que ativou o freio.
FREIO_QUARENTENA_INICIAL = 6

# Duração adicional da quarentena (em meses) se o ativo ativar o freio novamente.
FREIO_QUARENTENA_ADICIONAL = 12
