import os

import pandas as pd
import numpy as np
import requests
import bs4

import utils.misc as misc

url = 'https://fiis.com.br/filtro'
payload = {
    "exnome": "on",
    "exmercado": "on",
    "flmercadobolsa": "on",
    "flmercadobalcao": "on",
    "expublico": "on",
    "flpublicogeral": "on",
    "flpublicoiq": "on",
    "extipo": "on",
    "fltipo16": "on",
    "fltipo10": "on",
    "fltipo12": "on",
    "fltipo2": "on",
    "fltipo15": "on",
    "fltipo5": "on",
    "fltipo1": "on",
    "fltipo14": "on",
    "fltipo6": "on",
    "fltipo9": "on",
    "fltipo11": "on",
    "fltipo3": "on",
    "fltipo4": "on",
    "fltipo7": "on",
    "fltipo13": "on",
    "fltipo8": "on",
    "exadm": "on",
    "fladm1": "on",
    "fladm2": "on",
    "fladm39": "on",
    "fladm3": "on",
    "fladm33": "on",
    "fladm32": "on",
    "fladm4": "on",
    "fladm5": "on",
    "fladm6": "on",
    "fladm7": "on",
    "fladm8": "on",
    "fladm9": "on",
    "fladm10": "on",
    "fladm11": "on",
    "fladm31": "on",
    "fladm12": "on",
    "fladm13": "on",
    "fladm14": "on",
    "fladm0": "on",
    "fladm15": "on",
    "fladm16": "on",
    "fladm38": "on",
    "fladm17": "on",
    "fladm28": "on",
    "fladm18": "on",
    "fladm19": "on",
    "fladm20": "on",
    "fladm35": "on",
    "fladm30": "on",
    "fladm21": "on",
    "fladm37": "on",
    "fladm22": "on",
    "fladm29": "on",
    "fladm23": "on",
    "fladm24": "on",
    "fladm36": "on",
    "fladm25": "on",
    "fladm34": "on",
    "fladm26": "on",
    "fladm27": "on",
    "exfechamento": "on",
    "exurendrs": "on",
    "exurendper": "on",
    "urendpermin": "",
    "urendpermax": "",
    "exdatapag": "on",
    "exdatabase": "on",
    "exrendmedrs": "on",
    "exrendmedper": "on",
    "rendmedpermin": "",
    "rendmedpermax": "",
    "exppc": "on",
    "expvp": "on",
    "pvpmin": "",
    "pvpmax": "",
    "exnneg": "on",
    "nnegmin": "",
    "txpl": "on",
    "txrec": "on",
    "txvm": "on",
    "txvs": "on",
    "txrs": "on",
    "ordenapor": "codneg",
    "ordena1": "ASC"
}
response = requests.post(url, data=payload)

soup = bs4.BeautifulSoup(response.content, 'html5lib')
table = soup.find_all('table')[0]

tb_fii = pd.read_html(str(table), decimal=",", thousands=".")[0]
tb_fii = tb_fii.rename(str.lower, axis='columns')

nome = f'analise_fii.xlsx'
out = misc.cria_tabela(nome)
misc.add_planilha(out, 'fiis', tb_fii)


url = 'https://www.fundsexplorer.com.br/ranking'
response = requests.get(url)
soup = bs4.BeautifulSoup(response.text, 'html5lib')
table = soup.find_all('table')[0]

tb_fs = pd.read_html(str(table), decimal=",", thousands=".")[0]
tb_fs = tb_fs.rename(str.lower, axis='columns')

dicionario = {
    'códigodo fundo': 'papel',
    'preço atual': 'preco',
    'volume (21d)': 'liquidez',    
    'dividendyield': 'dy',
    'dy (3m)acumulado': 'dy3a',
    'dy (6m)acumulado': 'dy6a',
    'dy (12m)acumulado': 'dy12a',
    'dy (3m)média': 'dy3m',
    'dy (6m)média': 'dy6m',
    'dy (12m)média': 'dy12m',
    'dy ano': 'dyano',
    'variação preço': 'varpreco',
    'rentab.período': 'rent',
    'rentab.acumulada': 'rentacc',
    'patrimôniolíq.': 'patrimonio',
    'variaçãopatrimonial': 'varpatrimonial',
    'rentab. patr.no período': 'rentpatrimonial',
    'rentab. patr.acumulada': 'rentpatrimonialacc',
    'vacânciafísica': 'vfisica',
    'vacânciafinanceira': 'vfinanceira',
    'quantidadeativos': 'qtdativos'
}
tb_fs = tb_fs.rename(index=str, columns=dicionario)

tb_fs['dividendo'] = tb_fs['dividendo'].str.lstrip('R$').str.replace(',', '.').astype(float)
tb_fs['dy'] = tb_fs['dy'].str.rstrip('%').str.replace(',', '.').astype(float)

tb_fs['dy3a'] = tb_fs['dy3a'].str.rstrip('%').str.replace(',', '.').astype(float)
tb_fs['dy6a'] = tb_fs['dy6a'].str.rstrip('%').str.replace(',', '.').astype(float)
tb_fs['dy12a'] = tb_fs['dy12a'].str.rstrip('%').str.replace(',', '.').astype(float)

tb_fs['dy3m'] = tb_fs['dy3m'].str.rstrip('%').str.replace(',', '.').astype(float)
tb_fs['dy6m'] = tb_fs['dy6m'].str.rstrip('%').str.replace(',', '.').astype(float)
tb_fs['dy12m'] = tb_fs['dy12m'].str.rstrip('%').str.replace(',', '.').astype(float)

tb_fs['dyano'] = tb_fs['dyano'].str.rstrip('%').str.replace(',', '.').astype(float)
tb_fs['dypatrimonial'] = tb_fs['dypatrimonial'].str.rstrip('%').str.replace(',', '.').astype(float)
tb_fs['varpatrimonial'] = tb_fs['varpatrimonial'].str.rstrip('%').str.replace('.', '').str.replace(',', '.').astype(float)
tb_fs['rentpatrimonial'] = tb_fs['rentpatrimonial'].str.rstrip('%').str.replace('.', '').str.replace(',', '.').astype(float)
tb_fs['rentpatrimonialacc'] = tb_fs['rentpatrimonialacc'].str.rstrip('%').str.replace('.', '').str.replace(',', '.').astype(float)


tb_fs['varpreco'] = tb_fs['varpreco'].str.rstrip('%').str.replace('.', '').str.replace(',', '.').astype(float)
tb_fs['rent'] = tb_fs['rent'].str.rstrip('%').str.replace('.', '').str.replace(',', '.').astype(float)
tb_fs['rentacc'] = tb_fs['rentacc'].str.rstrip('%').str.replace('.', '').str.replace(',', '.').astype(float)

tb_fs['patrimonio'] = tb_fs['patrimonio'].str.lstrip('R$').str.replace('.', '').str.replace(',', '.').astype(float)
tb_fs['vpa'] = tb_fs['vpa'].str.lstrip('R$').str.replace('.', '').str.replace(',', '.').astype(float)

tb_fs['vfisica'] = tb_fs['vfisica'].str.rstrip('%').str.replace(',', '.').astype(float)
tb_fs['vfinanceira'] = tb_fs['vfinanceira'].str.rstrip('%').str.replace(',', '.').astype(float)


misc.add_planilha(out, 'fundsexplorer', tb_fs)
misc.salva_tabela(out)
