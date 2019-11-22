# encoding=utf8
import os
from datetime import datetime

import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt

# 'Date(2017, 10, 27, 0, 0, 0)'
def formata_data(dado):
    data = dado[0]

    tmp = data.split('(')[1]
    segmentacao = tmp.split(',')

    ano = int(segmentacao[0])
    mes = int(segmentacao[1]) + 1
    dia = int(segmentacao[2])

    return [datetime(ano, mes, dia), dado[1]]


ativo = 'MDIA3'
url = f'https://www.oceans14.com.br/rendaVariavel/respostaAjax/gHistoricoPl.aspx?papel={ativo}&periodo=5a'

headers = {
    'pragma': 'no-cache',
    'cookie': 'uid=BD9D750EBCB841FECD86D43EF925DA2D; origem=https://www.google.com/; ASP.NET_SessionId=01zsckrt1n5c20wpv2i12um2; contadorViewsAcoes=4',
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'authority': 'www.oceans14.com.br',
    'referer': 'https://www.oceans14.com.br/acoes/itausa/itsa/balanco-dividendos'
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()

    if data is not None:
        dados = list(map(lambda x: [x['c'][0]['v'], x['c'][1]['v']], data['rows']))
        dados = list(map(formata_data, dados))

        df = pd.DataFrame(dados, columns=['data', 'pl']) 
        # df['3d'] = df['pl'].rolling(3).mean()
        # df['7d'] = df['pl'].rolling(7).mean()
        df['30d'] = df['pl'].rolling(30).mean()
        df['90d'] = df['pl'].rolling(90).mean()
        df['200d'] = df['pl'].rolling(200).mean()
        df = df.set_index('data')

        pl_min = df['pl'].min()
        pl_max = df['pl'].max()

        print(f'PL - [{pl_min} {pl_max}]')

        ultimo = df.tail(1)
        # import ipdb; ipdb.set_trace()
        print()
        print(f'Sobrepreço em relação ao PLmin:',  ultimo['pl'] / pl_min)
        print(f'Sobrepreço em relação ao PLmax:', ultimo['pl'] / pl_max)
        print()
        print(f'Sobrepreço em relação ao PL30d:', ultimo['pl'] / ultimo['30d'])
        print(f'Sobrepreço em relação ao PL90d:', ultimo['pl'] / ultimo['90d'])
        print(f'Sobrepreço em relação ao PL200d:', ultimo['pl'] / ultimo['200d'])

