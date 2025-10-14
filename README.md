# Backtest de Estratégias de Investimento

Este projeto consiste em um script Python para realizar backtests de estratégias de investimento em ações brasileiras.

## Visão Geral do Projeto

O script `main.py` foi projetado para simular e analisar o desempenho de duas estratégias de investimento distintas em um portfólio de ações definido pelo usuário. Ele utiliza `yfinance` para baixar dados históricos de ações, `python-bcb` para buscar indicadores econômicos brasileiros (Selic e IPCA), `pandas` para análise de dados e `matplotlib` para visualizar os resultados.

## Funcionalidades

O script executa dois cenários de backtesting distintos:

1.  **Cenário 1: Aporte Único (Lump-Sum)**
    *   Simula um investimento de montante fixo inicial, distribuído igualmente entre uma lista predefinida de ações.
    *   Segue uma estratégia "buy and hold", reinvestindo automaticamente quaisquer dividendos recebidos.
    *   O desempenho do portfólio é comparado com a taxa Selic.

2.  **Cenário 2: Aportes Mensais**
    *   Começa com um saldo zero e simula contribuições mensais regulares.
    *   O valor da contribuição começa em um valor base (por exemplo, R$ 1000) e é ajustado mensalmente pela inflação (IPCA).
    *   Cada contribuição mensal é investida em um único ativo: aquele com o menor valor monetário total na carteira no momento do investimento.
    *   **Funcionalidade Freio de Arrumação:** Este cenário agora inclui um mecanismo de "freio de arrumação" inspirado na metodologia Bastter.com. Se um ativo receber mais de uma contribuição dentro de um período configurável, ele é colocado em "quarentena" por uma duração definida, evitando novos investimentos nele e, assim, prevenindo a concentração.
    *   Este portfólio também é comparado com a Selic, considerando as mesmas contribuições mensais.

## Instalação

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2.  **Instale as dependências:**

    Você precisa ter o Python 3.6+ instalado. As dependências podem ser instaladas usando `pip` e o arquivo `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

## Uso

Para executar os backtests, execute o script `main.py` a partir do seu terminal:

```bash
python main.py
```

O script executará ambos os cenários sequencialmente e exibirá três janelas de plotagem no final. O console mostrará um resumo detalhado dos resultados para cada cenário, incluindo comparações com o benchmark Selic.

## Configuração

Todos os parâmetros para o backtest (tickers de ações, valores de investimento, datas) são definidos no arquivo `config.py`. Isso inclui novas configurações para habilitar e ajustar o recurso de freio de arrumação (`FREIO_ATIVO`, `FREIO_PERIODO_APORTES`, `FREIO_QUARENTENA_INICIAL`, `FREIO_QUARENTENA_ADICIONAL`). Para executar diferentes cenários, você precisará modificar as variáveis neste arquivo diretamente.

## Saída

O script gera a seguinte saída:

*   **Console:** Resumos detalhados para ambos os cenários.
*   **Arquivos Excel:**
    *   `backtest_results_lump_sum.xlsx`: Resultados para o cenário de aporte único.
    *   `backtest_results_monthly.xlsx`: Resultados para o cenário de aportes mensais.
*   **Gráficos:** Três gráficos do `matplotlib` mostrando as curvas de capital e a distribuição das contribuições.
