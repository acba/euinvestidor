import os

import bs4
import pandas as pd
import numpy as np
import requests
import ipdb

def _conv_col_to_num(val):
    return pd.to_numeric(val.str.lstrip('R$').str.rstrip('%').str.replace('.', '').str.replace(',', '.'))


def get_table_fiis():

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
    tb_fii = tb_fii.drop(columns=['mercado', 'publico', 'último rendimento r$',
                                  'rendimento médio 12 meses r$', 'patrimônio / cota',
                                  'data pagamento', 'data base'])

    dicionario = {
        'código': 'papel', 
        'administrador': 'admin',
        'cotação base': 'preco',
        'último rendimento %': 'dy',
        # 'data pagamento': 'dt_pgt',
        # 'data base': 'dt_base',
        'rendimento médio 12 meses %': 'dy12m',
        # 'patrimônio / cota',
        'cotação / patrimônio': 'p/vpa',
        'nº médio de negócios / mês': 'liquidez',
    }
    tb_fii = tb_fii.rename(index=str, columns=dicionario)

    return tb_fii

def get_table_funds_explorer():

    url = 'https://www.fundsexplorer.com.br/ranking'
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html5lib')
    table = soup.find_all('table')[0]

    tb_fs = pd.read_html(str(table), decimal=",", thousands=".")[0]
    tb_fs = tb_fs.rename(str.lower, axis='columns')

    dicionario = {
        'códigodo fundo': 'papel',
        'preço atual': 'preco',
        'liquidez diária': 'liquidez',
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

    tb_fs['preco']              = _conv_col_to_num(tb_fs['preco'])
    tb_fs['dividendo']          = _conv_col_to_num(tb_fs['dividendo'])
    tb_fs['dy']                 = _conv_col_to_num(tb_fs['dy'])

    tb_fs['dy3a']               = _conv_col_to_num(tb_fs['dy3a'])
    tb_fs['dy6a']               = _conv_col_to_num(tb_fs['dy6a'])
    tb_fs['dy12a']              = _conv_col_to_num(tb_fs['dy12a'])

    tb_fs['dy3m']               = _conv_col_to_num(tb_fs['dy3m'])
    tb_fs['dy6m']               = _conv_col_to_num(tb_fs['dy6m'])
    tb_fs['dy12m']              = _conv_col_to_num(tb_fs['dy12m'])

    tb_fs['dyano']              = _conv_col_to_num(tb_fs['dyano'])
    tb_fs['dypatrimonial']      = _conv_col_to_num(tb_fs['dypatrimonial'])
    tb_fs['varpatrimonial']     = _conv_col_to_num(tb_fs['varpatrimonial'])
    tb_fs['rentpatrimonial']    = _conv_col_to_num(tb_fs['rentpatrimonial'])
    tb_fs['rentpatrimonialacc'] = _conv_col_to_num(tb_fs['rentpatrimonialacc'])


    tb_fs['varpreco']           = _conv_col_to_num(tb_fs['varpreco'])
    tb_fs['rent']               = _conv_col_to_num(tb_fs['rent'])
    tb_fs['rentacc']            = _conv_col_to_num(tb_fs['rentacc'])

    tb_fs['patrimonio']         = _conv_col_to_num(tb_fs['patrimonio'])
    tb_fs['vpa']                = _conv_col_to_num(tb_fs['vpa'])
    tb_fs['vfisica']            = _conv_col_to_num(tb_fs['vfisica'])
    tb_fs['vfisica']            = tb_fs['vfisica'].fillna(0)
    tb_fs['vfinanceira']        = _conv_col_to_num(tb_fs['vfinanceira'])
    tb_fs['vfinanceira']        = tb_fs['vfinanceira'].fillna(0)

    tb_fs['dy6m_adj']           = tb_fs['dy6m']*(1 + tb_fs['vfisica']/100)*(1 + tb_fs['vfinanceira']/100)
    tb_fs['liquidez']           = tb_fs['liquidez']/10

    return tb_fs


def get_tb_upside(tb):
    df = tb.copy()

    df = df[df['dyano'] > 0]
    df = df[df['liquidez'] > 0]
    df = df[df['p/vpa'] > 0]

    idka_pre_1a = 6.5799
    ir = 0.175
    premio = 2
    ms = .2

    txminima_anual = idka_pre_1a * (1 - ir) + premio
    txminima_mensal = (np.power( 1 + txminima_anual/100, 1/12 ) - 1)*100
    distribuicao_media_mensal = df['preco'] * (df['dy12m']/100)
    
    df['vi'] = distribuicao_media_mensal / (txminima_mensal/100)
    df['ms'] = df['vi'] * (1 - ms)
    df['upside'] = 100 * ((df['ms'] / df['preco']) - 1)

    return df

def get_tb_pvpa_rent(tb):
    df = tb.copy()

    df = df[df['dyano'] > 0]
    df = df[df['liquidez'] > 100]
    df = df[df['p/vpa'] > 0]

    df = df.sort_values(by=['p/vpa'])
    df['rank_pvpa'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df = df.sort_values(by=['rentacc'], ascending=False)
    df['rank_rent'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df['rank'] = df['rank_pvpa'] + df['rank_rent']
    df = df.sort_values(by=['rank'])

    return df

def get_tb_pvpa_dy12m(tb):
    df = tb.copy()

    df = df[df['dyano'] > 0]
    df = df[df['liquidez'] > 100]
    df = df[df['p/vpa'] > 0]

    df = df.sort_values(by=['p/vpa'])
    df['rank_pvpa'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df = df.sort_values(by=['dy12m'], ascending=False)
    df['rank_dy12m'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df['rank'] = df['rank_pvpa'] + df['rank_dy12m']
    df = df.sort_values(by=['rank'])

    return df

def get_tb_pvpa_dy6m_adj(tb):
    df = tb.copy()

    df = df[df['dyano'] > 0]
    df = df[df['liquidez'] > 100]
    df = df[df['p/vpa'] > 0]

    df = df.sort_values(by=['p/vpa'])
    df['rank_pvpa'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df = df.sort_values(by=['dy6m_adj'], ascending=False)
    df['rank_dy6m_adj'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df['rank'] = df['rank_pvpa'] + df['rank_dy6m_adj']
    df = df.sort_values(by=['rank'])

    return df
