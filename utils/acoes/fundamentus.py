import pandas as pd
import requests


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


def get_url(setor):
    code = _get_setor_code(setor)

    url = None
    if setor == 'geral':
        url = 'http://www.fundamentus.com.br/resultado.php'
    else:
        url = f'http://www.fundamentus.com.br/resultado.php?setor={code}'

    return url


def _conv_column(col):
    return pd.to_numeric(col.str.replace('.', '').str.replace('%', '').str.replace(',', '.'))


def get_table(setor):

    url = get_url(setor)

    headers = {
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    response = requests.get(url, headers=headers)

    tb = pd.read_html(response.text, decimal=",", thousands=".")[0]
    tb = tb.rename(str.lower, axis='columns')

    dicionario = {
        'papel': 'ticker',
        'cotação': 'preco',
        'div.yield': 'dy',
        'p/ativ circ.liq': 'p/ativocl',
        'mrg ebit': 'margemEbit',
        'mrg. líq.': 'margemLiquida',
        'liq. corr.': 'liquidezCorrente',
        'liq.2meses': 'liquidez',
        'patrim. líq': 'pl',
        'dív.brut/ patrim.': 'db/pl',
        'cresc. rec.5a': 'cresc5_rl'
    }
    tb = tb.rename(index=str, columns=dicionario)

    tb = tb[tb['liquidez'] > 1000]

    tb['dy'] = _conv_column(tb['dy'])
    tb['margemEbit'] = _conv_column(tb['margemEbit'])
    tb['margemLiquida'] = _conv_column(tb['margemLiquida'])
    tb['roic'] = _conv_column(tb['roic'])
    tb['roe'] = _conv_column(tb['roe'])
    tb['cresc5_rl'] = _conv_column(tb['cresc5_rl'])

    ordem = ['ticker', 'preco', 'p/l', 'p/vp', 'ev/ebitda',
             'dy', 'roe', 'margemLiquida', 'margemEbit', 'cresc5_rl']
    resto = list(set(tb.columns.tolist()) - set(ordem))

    tb = tb[ordem + resto]

    print(tb.head())
    print(tb.dtypes)

    return tb
