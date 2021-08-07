# encoding=utf8
import os
import sys 

from datetime import datetime
import ipdb

import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt

# 'Date(2017, 10, 27, 0, 0, 0)'
def formata_data(dado):
    data = dado[0]

    segmentacao = data.split('/')
    
    dia = int(segmentacao[0])
    mes = int(segmentacao[1])
    ano = int(segmentacao[2])

    dado_normalizado = dado[1] if dado[1] > 0 else 0

    try:
        res = [datetime(ano, mes, dia), dado_normalizado]
    except:
        import ipdb; ipdb.set_trace()

    return res

def get_recomendacao(dado):
    if dado < -15:
        return 'COMPRA FORTE'
    elif dado < -5:
        return 'COMPRA'
    elif dado >= -5 and dado < 5:
        return 'NEUTRO'
    elif dado < 15:
        return 'VENDA'
    else:
        return 'VENDA FORTE'

# ativo = sys.argv[1] if len(sys.argv) >= 2 and sys.argv[1] is not None else 'CPLE3'
# periodo = sys.argv[2] if len(sys.argv) >= 3 and sys.argv[2] is not None else '5a'

ativo   = 'BBAS3'
periodo = '5a'

url = f'https://www.oceans14.com.br/rendaVariavel/respostaAjax/gHistoricoPl.aspx?papel={ativo}&periodo={periodo}'

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
        dados = list(map(lambda x: [x['data'], x['pl']], data))
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
        ultimo = df.tail(1)

        print(f'PL Atual - {ultimo["pl"][0]}')
        print(f'PLMin PLMax - [{pl_min} {pl_max}]')
        print(f'PL30d PL90d PL200d - [{np.around(ultimo["30d"][0], decimals=2)} {np.around(ultimo["90d"][0], decimals=2)} {np.around(ultimo["200d"][0], decimals=2)}]')

        s_plmin = np.around(((ultimo['pl'][0]/pl_min - 1) * 100), decimals=2)
        s_plmax = np.around(((ultimo['pl'][0]/pl_max - 1) * 100), decimals=2)
        s_pl30d = np.around(((ultimo['pl'][0]/ultimo['30d'][0] - 1) * 100), decimals=2)
        s_pl90d = np.around(((ultimo['pl'][0]/ultimo['90d'][0] - 1) * 100), decimals=2)
        s_pl200d = np.around(((ultimo['pl'][0]/ultimo['200d'][0] - 1) * 100), decimals=2)
        
        print()
        print(f'Sobrepreço em relação ao PLmin: {s_plmin}%')
        print(f'Sobrepreço em relação ao PLmax: {s_plmax}%')
        print()
        print(f'{get_recomendacao(s_pl30d)} - Sobrepreço em relação ao PL30d : {s_pl30d}%')
        print(f'{get_recomendacao(s_pl90d)} - Sobrepreço em relação ao PL90d : {s_pl90d}%')
        print(f'{get_recomendacao(s_pl200d)} - Sobrepreço em relação ao PL200d: {s_pl200d}%')

        df.to_excel(f'dados/{ativo}.xlsx')

        df.plot()
        plt.xlabel('Tempo')
        plt.ylabel('Preço/Lucro')
        plt.title(f'{ativo}'.upper())
        plt.savefig(f'dados/{ativo}.svg', format='svg', dpi=1200)