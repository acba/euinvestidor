import os
from pathlib import Path
from enum import Enum

import pandas as pd
import numpy as np
import requests
import ipdb

import utils.acoes.fundamentus as fundamentus
import utils.acoes.statusinvest as statusinvest

ROE_THRESHOLD = 5
LIQUIDEZ_THRESHOLD = 1000
PL_THRESHOLD = 0
PVP_THRESHOLD = 0


class Fontes(Enum):
    FUNDAMENTUS = 0
    STATUSINVEST = 1


def get_table(setor='geral', fonte=Fontes.FUNDAMENTUS):

    if fonte == Fontes.FUNDAMENTUS:
        return fundamentus.get_table(setor)
    elif fonte == Fontes.STATUSINVEST:
        return statusinvest.get_table(setor)


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

    # df = df[df['ev/ebitda'] >= 0]
    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]

    ms = .25

    df['vi'] = np.sqrt(22.5 / (df['p/l'] * df['p/vp'])) * df['preco']
    df['ms'] = df['vi'] * (1-ms)
    df['desconto'] = 1 - df['preco'] / df['vi']
    df['upside'] = 100 * ((df['ms'] / df['preco']) - 1)
    # df['ticket'] = df['papel'].str[:4]

    df = df.sort_values(by=['desconto'], ascending=False).reset_index()
    # df = df.groupby(['ticket']).first().reset_index()
    # df = df.sort_values(by=['desconto'], ascending=True)

    df['vi'] = df['vi'].round(2)
    df['ms'] = df['ms'].round(2)
    df['desconto'] = df['desconto'].round(2)
    df['upside'] = df['upside'].round(2)

    df = df.drop(columns=['index'])

    return df


def get_tb_num_graham_limpa(tb):
    df = tb.copy()

    df = df[df['cresc5a'] > -5]
    df = df[df['dy'] > 0]
    df = df[df['ev/ebitda'] >= 0]
    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]
    df = df[df['roe'] > 7]
    df = df[df['liquidez'] > 1000]

    ms = .25
    df['vi'] = np.sqrt(22.5 / (df['p/l'] * df['p/vp'])) * df['preco']
    df['ms'] = df['vi'] * (1-ms)
    df['desconto'] = df['preco'] / df['vi']
    df['upside'] = 100 * ((df['ms'] / df['preco']) - 1)
    df['ticket'] = df['papel'].str[:4]

    df = df.sort_values(by=['desconto'], ascending=True).reset_index()
    df = df.groupby(['ticket']).first().reset_index()
    df = df.sort_values(by=['desconto'], ascending=True)

    df = df.drop(columns=['ticket', 'index'])

    return df


def get_tb_graham_ajustado(tb):
    df = tb.copy()

    df = df[df['ev/ebitda'] >= 0]
    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]

    tx_livre_risco = 6
    df['vi'] = (df['preco']/df['p/l']) * (7 + df['cresc5a']) * 4.4 / 6
    df['ms'] = df['vi'] * .75
    df['desconto'] = df['preco'] / df['vi']
    df['upside'] = 100 * ((df['ms'] / df['preco']) - 1)
    df['ticket'] = df['papel'].str[:4]

    df = df.sort_values(by=['desconto'], ascending=True).reset_index()
    df = df.groupby(['ticket']).first().reset_index()
    df = df.sort_values(by=['desconto'], ascending=True)

    df = df.drop(columns=['ticket', 'index'])

    return df


# def get_tb_num_graham2(tb):
#     df = tb.copy()

#     df = df[df['p/l'] > 0]
#     df = df[df['p/vp'] > 0]
#     df = df[df['liquidez'] > 1000]

#     df['graham'] = df['preco'] / df['p/l'] * (8.5 + 2*df['cresc5a']/5) * 4.4 / 6.5
#     df['desconto'] = df['preco'] / df['graham']
#     df = df[df['preco'] < df['graham']].sort_values(by=['desconto'], ascending=True)

#     return df

# def get_tb_num_graham3(tb):
#     df = tb.copy()

#     df = df[df['p/l'] > 0]
#     df = df[df['p/vp'] > 0]
#     df = df[df['liquidez'] > 1000]

#     df['graham'] = np.sqrt(22.5 / (df['p/l'] * df['p/vp'])) * df['preco']
#     df['desconto'] = df['preco'] / df['graham']
#     df['upside'] = 100 * ((df['graham'] / df['preco']) - 1)

#     df = df[df['preco'] < 1.5 * df['graham']]

#     df = df.sort_values(by=['upside'], ascending=False)
#     df['rank_upside'] = pd.Series(np.arange(df.shape[0]), index=df.index)

#     df = df.sort_values(by=['p/l'])
#     df['rank_pl'] = pd.Series(np.arange(df.shape[0]), index=df.index)

#     df = df.sort_values(by=['roe'], ascending=False)
#     df['rank_roe'] = pd.Series(np.arange(df.shape[0]), index=df.index)

#     df['rank'] = df['rank_pl'] + df['rank_roe'] + df['rank_upside']

#     df = df.sort_values(by=['rank'], ascending=True)

#     return df

def get_tb_composta(tb):
    df = tb.copy()

    df = get_tb_num_graham_limpa(df)

    df = df.sort_values(by=['upside'], ascending=False)
    df['rank_graham'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df = df.sort_values(by=['p/l'])
    df['rank_pl'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df = df.sort_values(by=['roe'], ascending=False)
    df['rank_roe'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df = get_tb_psbe(df)
    df = df.sort_values(by=['upside'], ascending=False)
    df['rank_psbe'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df['rank'] = df['rank_pl'] + df['rank_roe'] + \
        df['rank_graham'] + df['rank_psbe']
    df = df.sort_values(by=['rank'], ascending=True)

    return df


def get_tb_peg(tb):
    df = tb.copy()

    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]
    df = df[df['liquidez'] > 1000]

    df['peg'] = df['p/l'] / df['cresc5a']
    df = df.sort_values(by=['peg'], ascending=True)

    df = df[df['peg'] > 0]

    return df


def get_tb_bazim(tb):
    df = tb.copy()

    df = df[df['dy'] > 6]
    df = df[df['liquidez'] > 1000]
    df = df[df['div/pat'] < 3]

    df['desconto'] = df['p/l'] / 16.666
    df = df.sort_values(by=['desconto'], ascending=True)

    return df


def get_tb_ev_roic(tb):
    df = tb.copy()

    df = df[df['liquidez'] > 1000]
    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]
    df = df[df['ev/ebitda'] >= 0]

    df = df.sort_values(by=['ev/ebitda'])
    df['rank_ev'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df = df.sort_values(by=['roic'], ascending=False)
    df['rank_roic'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df['rank_ev_roic'] = df['rank_ev'] + df['rank_roic']
    df = df.sort_values(by=['rank_ev_roic'])

    return df


def get_tb_psbe(tb):
    df = tb.copy()

    df = df[df['liquidez'] > 1000]
    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]
    df = df[df['ev/ebitda'] >= 0]
    # df = df[df['dy'] > 0]
    df = df[df['roe'] > 5]
    df = df[df['cresc5a'] > -5]

    # df = df.sort_values(by=['ev/ebitda'])
    # df['rank_ev'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    # df = df.sort_values(by=['roic'], ascending=False)
    # df['rank_roic'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    # df['rank_ev_roic'] = df['rank_ev'] + df['rank_roic']
    # df = df.sort_values(by=['rank_ev_roic'])

    df['ll'] = (df['roe']/100) * df['patrimonio']
    df['rl'] = df['ll'] / (df['mrg. líq.']/100)
    df['n'] = df['ll'] * df['p/l'] / df['preco']
    df['vm'] = df['n'] * df['preco']
    cte = 7
    # cte = 5.891

    margem_seguranca = .25
    df['psbe'] = (df['patrimonio'] + df['rl'] + df['ll'] * np.exp((df['mrg. líq.']/100)
                                                                  * -1 * np.log(np.abs(df['mrg. líq.']/100)) * cte * np.sign(df['mrg. líq.']))) / df['n']
    df['ms'] = df['psbe'] * (1 - margem_seguranca)
    df['upside'] = 100 * ((df['ms'] / df['preco']) - 1)

    df['psbe'] = df['psbe'].round(2)
    df['ms'] = df['ms'].round(2)
    df['upside'] = df['upside'].round(2)

    df['ticket'] = df['papel'].str[:4]

    df = df.sort_values(by=['upside'], ascending=False).reset_index()
    df = df.groupby(['ticket']).first().reset_index()

    df = df.sort_values(by=['upside'], ascending=False)
    df = df.drop(columns=['ll', 'rl', 'n', 'vm', 'ticket', 'index'])

    return df


def get_tb_fcd(tb):
    df = tb.copy()

    df = df[df['liquidez'] > 1000]
    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]
    df = df[df['ev/ebitda'] >= 0]
    df = df[df['roe'] > 5]
    df = df[df['cresc5a'] > -5]

    df['lpa'] = df['preco'] / df['p/l']
    tx_desconto = .09
    tx_perpetuidade = .03
    delta = tx_desconto - tx_perpetuidade

    tx_crescimento = df['cresc5a']/100
    tx_crescimento[tx_crescimento > 30] *= .6

    crescimento_ano_1 = tx_crescimento
    crescimento_ano_2 = tx_crescimento * .9
    crescimento_ano_3 = tx_crescimento * .9 * .9
    crescimento_ano_4 = tx_crescimento * .9 * .9 * .9
    crescimento_ano_5 = tx_crescimento * .9 * .9 * .9 * .9

    f1 = (np.power(1 + crescimento_ano_1, 1) / np.power(1+tx_desconto, 1))
    f2 = (np.power(1 + crescimento_ano_2, 2) / np.power(1+tx_desconto, 2))
    f3 = (np.power(1 + crescimento_ano_3, 3) / np.power(1+tx_desconto, 3))
    f4 = (np.power(1 + crescimento_ano_4, 4) / np.power(1+tx_desconto, 4))
    f5 = (np.power(1 + crescimento_ano_5, 5) / np.power(1+tx_desconto, 5))
    fator_fixo = (1 + tx_desconto) / delta

    df['preco_ano_1'] = df['lpa'] * f1 * fator_fixo
    df['preco_ano_2'] = df['lpa'] * (f1 + f2 * fator_fixo)
    df['preco_ano_3'] = df['lpa'] * (f1 + f2 + f3 * fator_fixo)
    df['preco_ano_4'] = df['lpa'] * (f1 + f2 + f3 + f4 * fator_fixo)
    df['preco_ano_5'] = df['lpa'] * (f1 + f2 + f3 + f4 + f5 * fator_fixo)

    margem_seguranca = .25

    df['ms'] = df['preco_ano_5'] * (1 - margem_seguranca)
    df['upside'] = 100 * ((df['ms'] / df['preco']) - 1)

    df['lpa'] = df['lpa'].round(2)
    df['preco_ano_1'] = df['preco_ano_1'].round(2)
    df['preco_ano_2'] = df['preco_ano_2'].round(2)
    df['preco_ano_3'] = df['preco_ano_3'].round(2)
    df['preco_ano_4'] = df['preco_ano_4'].round(2)
    df['preco_ano_5'] = df['preco_ano_5'].round(2)
    df['ms'] = df['ms'].round(2)
    df['upside'] = df['upside'].round(2)

    df['ticket'] = df['papel'].str[:4]

    df = df.sort_values(by=['upside'], ascending=False).reset_index()
    df = df.groupby(['ticket']).first().reset_index()

    df = df.sort_values(by=['upside'], ascending=False)
    df = df.drop(columns=['ticket', 'index'])

    return df


def get_tb_psbe_geral(tb):
    df = tb.copy()

    df = df[df['liquidez'] > 1000]
    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]

    df['ll'] = (df['roe']/100) * df['patrimonio']
    df['rl'] = df['ll'] / (df['mrg. líq.']/100)
    df['n'] = df['ll'] * df['p/l'] / df['preco']
    df['vm'] = df['n'] * df['preco']
    cte = 7
    # cte = 5.891

    margem_seguranca = .25
    df['psbe'] = (df['patrimonio'] + df['rl'] + df['ll'] * np.exp((df['mrg. líq.']/100)
                                                                  * -1 * np.log(np.abs(df['mrg. líq.']/100)) * cte * np.sign(df['mrg. líq.']))) / df['n']
    df['ms'] = df['psbe'] * (1 - margem_seguranca)
    df['upside'] = 100 * ((df['ms'] / df['preco']) - 1)

    df['psbe'] = df['psbe'].round(2)
    df['ms'] = df['ms'].round(2)
    df['upside'] = df['upside'].round(2)

    df['ticket'] = df['papel'].str[:4]

    df = df.sort_values(by=['upside'], ascending=False).reset_index()
    df = df.groupby(['ticket']).first().reset_index()

    df = df.sort_values(by=['upside'], ascending=False)
    df = df.drop(columns=['ll', 'rl', 'n', 'vm', 'ticket', 'index'])

    return df
