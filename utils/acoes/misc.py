import os
from pathlib import Path

import pandas as pd
import numpy as np
import requests
import ipdb



def _get_setor_code(setor):
    _setor = {
        'geral': '',
        'Petróleo, Gás e Biocombustíveis': '1',
        'Mineração': '2',
        'Previdência e Seguros': '38',
        'Alimentos': '15',
        'bancos': '35',
        'eletricas': '32',
    }
    try:
        return _setor[setor]

    except KeyError:
        return None


def get_url(setor_analise):
    code = _get_setor_code(setor_analise)

    url = None
    if setor_analise == 'geral':
        url = 'http://www.fundamentus.com.br/resultado.php'
    else:
        url = f'http://www.fundamentus.com.br/resultado.php?setor={code}'

    return url

def _conv_column(col):
    return pd.to_numeric(col.str.replace('.', '').str.replace('%', '').str.replace(',', '.'))

def get_table(url):

    headers = {
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    response = requests.get(url, headers=headers)

    tb = pd.read_html(response.text, decimal=",", thousands=".")[0]
    tb = tb.rename(str.lower, axis='columns')
    tb = tb.drop(columns=['p/ativo', 'p/cap.giro', 'p/ebit', 'p/ativ circ.liq', 'liq. corr.', 'psr'])

    dicionario = {
        "cotação": "preco",
        'div.yield': 'dy',
        'liq.2meses': 'liquidez',
        'patrim. líq': 'patrimonio',
        'dív.brut/ patrim.': 'div/pat',
        'cresc. rec.5a': 'cresc5a'
    }
    tb = tb.rename(index=str, columns=dicionario)

    tb              = tb[tb['liquidez'] > 0]

    tb['dy']        = _conv_column(tb['dy'])
    tb['mrg ebit']  = _conv_column(tb['mrg ebit'])
    tb['mrg. líq.'] = _conv_column(tb['mrg. líq.'])
    tb['roic']      = _conv_column(tb['roic'])
    tb['roe']       = _conv_column(tb['roe'])
    tb['cresc5a']   = _conv_column(tb['cresc5a'])

    print(tb.head())
    print(tb.dtypes)

    # # Tratando dados
    # tb['Mrg Ebit']      = pd.to_numeric(tb['Mrg Ebit'].str.replace('.', '').str.replace('%','').str.replace(',','.'))
    # tb['Mrg. Líq.']     = pd.to_numeric(tb['Mrg. Líq.'].str.replace('.', '').str.replace('%','').str.replace(',','.'))
    # tb['ROIC']          = pd.to_numeric(tb['ROIC'].str.replace('.', '').str.replace('%','').str.replace(',','.'))
    # tb['ROE']           = pd.to_numeric(tb['ROE'].str.replace('.', '').str.replace('%','').str.replace(',','.'))
    # tb['Cresc. Rec.5a'] = pd.to_numeric(tb['Cresc. Rec.5a'].str.replace('.', '').str.replace('%','').str.replace(',','.'))

    return tb

def cria_tabela(filename):
    _cria_outdir()
    path = Path(_get_outdir())
    fullpath = path / filename

    return pd.ExcelWriter(str(fullpath))

def add_planilha(writer, nome_planilha, tb):
    tb.to_excel(writer, nome_planilha, index=False)

def salva_tabela(writer):
    writer.save()

def _get_outdir():
    return './dados/'

def _cria_outdir():
    path = _get_outdir()
    if not os.path.exists(path):
        os.makedirs(path)

def get_tb_num_graham_puro(tb):
    df = tb.copy()

    df['vi'] = np.sqrt(22.5 / (df['p/l'] * df['p/vp'])) * df['preco']
    df['ms'] = df['vi'] * .8
    df['desconto'] = df['preco'] / df['vi']
    df['upside'] = 100 * ((df['ms'] / df['preco']) - 1)
    df['ticket'] = df['papel'].str[:4]

    df = df.sort_values(by=['desconto'], ascending=True).reset_index()
    df = df.groupby(['ticket']).first().reset_index()    
    df = df.sort_values(by=['desconto'], ascending=True)

    return df

def get_tb_num_graham(tb):
    df = tb.copy()

    df = df[df['cresc5a'] > -5]
    df = df[df['dy'] > 0]
    df = df[df['ev/ebit'] >= 0]
    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]
    df = df[df['roe'] > 7]
    df = df[df['liquidez'] > 100000]

    df['vi'] = np.sqrt(22.5 / (df['p/l'] * df['p/vp'])) * df['preco']
    df['ms'] = df['vi'] * .8
    df['desconto'] = df['preco'] / df['vi']
    df['upside'] = 100 * ((df['ms'] / df['preco']) - 1)
    df['ticket'] = df['papel'].str[:4]

    df = df.sort_values(by=['desconto'], ascending=True).reset_index()
    df = df.groupby(['ticket']).first().reset_index()    
    df = df.sort_values(by=['desconto'], ascending=True)

    return df

def get_tb_num_graham3(tb):
    df = tb.copy()

    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]
    df = df[df['liquidez'] > 10000]

    df['graham'] = np.sqrt(22.5 / (df['p/l'] * df['p/vp'])) * df['preco']
    df['desconto'] = df['preco'] / df['graham']
    df['upside'] = 100 * ((df['graham'] / df['preco']) - 1)

    df = df[df['preco'] < 1.5 * df['graham']]

    df = df.sort_values(by=['upside'], ascending=False)
    df['rank_upside'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df = df.sort_values(by=['p/l'])
    df['rank_pl'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df = df.sort_values(by=['roe'], ascending=False)
    df['rank_roe'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df['rank'] = df['rank_pl'] + df['rank_roe'] + df['rank_upside']

    df = df.sort_values(by=['rank'], ascending=True)

    return df

def get_tb_num_graham2(tb):
    df = tb.copy()

    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]
    df = df[df['liquidez'] > 10000]

    df['graham'] = df['preco'] / df['p/l'] * (8.5 + 2*df['cresc5a']/5) * 4.4 / 6.5
    df['desconto'] = df['preco'] / df['graham']
    df = df[df['preco'] < df['graham']].sort_values(by=['desconto'], ascending=True)

    return df

def get_tb_peg(tb):
    df = tb.copy()

    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]
    df = df[df['liquidez'] > 10000]

    df['peg'] = df['p/l'] / df['cresc5a']
    df = df.sort_values(by=['peg'], ascending=True)

    return df

def get_tb_bazim(tb):
    df = tb.copy()

    df = df[df['dy'] > 6]
    df = df[df['liquidez'] > 10000]
    df = df[df['div/pat'] < 3]

    df['desconto'] = df['p/l'] / 16.666
    df = df.sort_values(by=['desconto'], ascending=True)

    return df

def get_tb_ev_roic(tb):
    df = tb.copy()

    df = df[df['liquidez'] > 10000]
    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]
    df = df[df['ev/ebit'] > 0]

    df = df.sort_values(by=['ev/ebit'])
    df['rank_ev'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df = df.sort_values(by=['roic'], ascending=False)
    df['rank_roic'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df['rank_ev_roic'] = df['rank_ev'] + df['rank_roic']
    df = df.sort_values(by=['rank_ev_roic'])

    return df

