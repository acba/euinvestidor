import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt


def get_url(ativo):
    return f'https://api-analitica.sunoresearch.com.br/api/Indicator/GetIndicatorsYear?ticker={ativo}'


def get_table(ativo):
    url = get_url(ativo)
    headers = {
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    }

    res = requests.get(url, headers=headers)
    df = pd.read_json(res.text)

    return df

ativo = 'SULA4'

df = get_table(ativo)

# Tabela contendo os dividendos recebidos no ano
div_anual = df[['year', 'dpa']]

df.to_csv(f'dados/{ativo}.csv')