import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt


def get_url(ativo):
    return f'http://www.fundamentus.com.br/proventos.php?papel={ativo}&tipo=2'


def get_table(ativo):
    url = get_url(ativo)
    res = requests.get(url)

    df = pd.read_html(res.text, decimal=",", thousands=".", parse_dates=[0])[0]
    df.columns = ['data', 'valor', 'tipo', 'fator']
    df['ticker'] = ativo
    df['ano'] = df['data'].dt.year
    df['mes'] = df['data'].dt.month
    df['valor'] = df['valor'] / df['fator']

    df = df[['ticker', 'data', 'ano', 'mes', 'valor', 'tipo']]

    return df


def cagr(anual, periodo='all'):
    if periodo == 'all':
        periodo = anual.shape[0] - 1

    if periodo > anual.shape[0]:
        return np.nan

    fim = anual.iloc[-1, 0]
    idx = -1 * periodo - 1
    inicio = anual.iloc[idx, 0]

    return [100 * ((fim/inicio)**(1/periodo) - 1), inicio, fim]


def mt_cagr(anual):
    periodos = [1, 3, 5, 10, 'all']

    d = {}
    for p in periodos:
        d[str(p)] = cagr(anual, p)

    df = pd.DataFrame(d)
    df.columns = ['1yr', '3yr', '5yr', '10yr', 'todos']

    return df


def mt_ddm(cagr, div_anual):
    tx_10yr = cagr['10yr'].iloc[0]

    ultimo_div = (1 + tx_10yr/100) * div_anual.iloc[-1, 0]
    tx_retorno = 10
    tx_crescimento = tx_10yr

    return 100 * ultimo_div / (tx_retorno - tx_crescimento)


ativo = 'TAEE11'

df = get_table(ativo)

# Tabela contendo os dividendos recebidos no ano
div_anual = df[['ano', 'valor']].groupby('ano').sum()

# Tabela contendo o CAGR de 1, 3, 5, 10 e total do dividendos
cagr = mt_cagr(div_anual)

# Valuation
ddm = mt_ddm(cagr, div_anual)
print('ddm', ddm)

# Tabela contendo o incremento de um ano pro outro nos dividendos
incrementos = div_anual['valor'] / div_anual['valor'].shift(1) - 1
# incrementos.plot()
# plt.show()
