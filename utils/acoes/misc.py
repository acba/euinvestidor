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

TAXA_SELIC = 3
MARGEM_SEGURANCA = .25

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

def calcula_planilhas(out, tb, fonte, prefix):

    add_planilha(out, fonte, tb)

    tb_num_graham_puro = get_tb_num_graham_puro(tb)
    tb_num_graham_rentavel = get_tb_num_graham_rentaveis(tb)
    tb_num_graham_ajustado = get_tb_graham_ajustado(tb)
    tb_peg = get_tb_peg(tb)
    tb_ev_roic = get_tb_ev_roic(tb)
    tb_psbe = get_tb_psbe(tb)
    tb_fcd = get_tb_fcd(tb)

    tb_geral = pd.merge(tb_num_graham_puro[['ticker', 'rank']], tb_num_graham_rentavel[['ticker', 'rank']], on='ticker', how='outer')
    tb_geral = pd.merge(tb_geral, tb_num_graham_ajustado[['ticker', 'rank']], on='ticker', how='outer')
    tb_geral = pd.merge(tb_geral, tb_peg[['ticker', 'rank']], on='ticker', how='outer')
    tb_geral = pd.merge(tb_geral, tb_ev_roic[['ticker', 'rank']], on='ticker', how='outer')
    tb_geral = pd.merge(tb_geral, tb_psbe[['ticker', 'rank']], on='ticker', how='outer')
    tb_geral = pd.merge(tb_geral, tb_fcd[['ticker', 'rank']], on='ticker', how='outer')
    tb_geral.columns = ['ticker', 'graham_puro', 'graham_rentavel', 'graham_ajustado', 'peg', 'ev_roic', 'psbe', 'fcd']
    tb_geral['rank'] = tb_geral.iloc[:, 1:].sum(axis=1)
    tb_geral['count'] = tb_geral.iloc[:, 1:].count(axis=1)

    tb_geral['mizera_indice'] = tb_geral['rank'] / tb_geral['count']
    tb_geral = tb_geral.sort_values(by=['mizera_indice']).reset_index()
    tb_geral = tb_geral.drop(columns=['index'])

    add_planilha(out, f'{prefix}graham', tb_num_graham_puro)
    add_planilha(out, f'{prefix}graham_rentaveis', tb_num_graham_rentavel)
    add_planilha(out, f'{prefix}graham_ajustado', tb_num_graham_ajustado)
    add_planilha(out, f'{prefix}peg', tb_peg)
    add_planilha(out, f'{prefix}ev_roic', tb_ev_roic)
    add_planilha(out, f'{prefix}psbe', tb_psbe)
    add_planilha(out, f'{prefix}fcd', tb_fcd)
    add_planilha(out, f'{prefix}geral', tb_geral)


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
    df = df[df['liquidez'] > LIQUIDEZ_THRESHOLD]

    df['vi'] = np.sqrt(22.5 / (df['p/l'] * df['p/vp'])) * df['preco']
    df['ms'] = df['vi'] * (1-MARGEM_SEGURANCA)
    df['desconto'] = 1 - df['preco'] / df['vi']
    df['upside'] = 100 * ((df['ms'] / df['preco']) - 1)
    df['empresa'] = df['ticker'].str[:4]

    df = df.sort_values(by=['desconto'], ascending=False).reset_index()
    df = df.groupby(['empresa']).first().reset_index()
    df = df.sort_values(by=['desconto'], ascending=False)

    df['vi'] = df['vi'].round(2)
    df['ms'] = df['ms'].round(2)
    df['desconto'] = df['desconto'].round(2)
    df['upside'] = df['upside'].round(2)
    df['rank'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df = df.drop(columns=['index', 'empresa'])

    return df


def get_tb_num_graham_rentaveis(tb):
    df = tb.copy()

    df = df[df['cagr'] > -5]
    # df = df[df['ev/ebitda'] >= 0]
    # df = df[df['dy'] > 0]
    if 'ev/ebitda' in df:
        df = df[df['ev/ebitda'] >= 0]
    if 'ev/ebit' in df:
        df = df[df['ev/ebit'] >= 0]

    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]
    df = df[df['roe'] > TAXA_SELIC]
    df = df[df['liquidez'] > LIQUIDEZ_THRESHOLD]

    df['vi'] = np.sqrt(22.5 / (df['p/l'] * df['p/vp'])) * df['preco']
    df['ms'] = df['vi'] * (1-MARGEM_SEGURANCA)
    df['desconto'] = 1 - df['preco'] / df['vi']
    df['upside'] = 100 * ((df['ms'] / df['preco']) - 1)
    df['empresa'] = df['ticker'].str[:4]

    df = df.sort_values(by=['desconto'], ascending=False).reset_index()
    df = df.groupby(['empresa']).first().reset_index()
    df = df.sort_values(by=['desconto'], ascending=False)

    df['vi'] = df['vi'].round(2)
    df['ms'] = df['ms'].round(2)
    df['desconto'] = df['desconto'].round(2)
    df['upside'] = df['upside'].round(2)
    df['rank'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df = df.drop(columns=['index', 'empresa'])

    return df


def get_tb_graham_ajustado(tb):
    df = tb.copy()

    if 'ev/ebitda' in df:
        df = df[df['ev/ebitda'] >= 0]
    if 'ev/ebit' in df:
        df = df[df['ev/ebit'] >= 0]
    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]
    df = df[df['liquidez'] > LIQUIDEZ_THRESHOLD]


    if df['cagr'] < TAXA_SELIC:
        cagr = TAXA_SELIC
    else:
        cagr = df['cagr']

    # df['vi'] = (df['preco']/df['p/l']) * (7 + cagr) * 4.4 / 6
    df['vi'] = (df['preco']/df['p/l']) * (6 + cagr)
    df['ms'] = df['vi'] *  (1-MARGEM_SEGURANCA)
    df['desconto'] = 1 - df['preco'] / df['vi']
    df['upside'] = 100 * ((df['ms'] / df['preco']) - 1)
    df['empresa'] = df['ticker'].str[:4]

    df = df.sort_values(by=['desconto'], ascending=False).reset_index()
    df = df.groupby(['empresa']).first().reset_index()
    df = df.sort_values(by=['desconto'], ascending=False)

    df['vi'] = df['vi'].round(2)
    df['ms'] = df['ms'].round(2)
    df['desconto'] = df['desconto'].round(2)
    df['upside'] = df['upside'].round(2)
    df['rank'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df = df.drop(columns=['empresa', 'index'])

    return df


# def get_tb_composta(tb):
#     df = tb.copy()

#     df = get_tb_num_graham_limpa(df)

#     df = df.sort_values(by=['upside'], ascending=False)
#     df['rank_graham'] = pd.Series(np.arange(df.shape[0]), index=df.index)

#     df = df.sort_values(by=['p/l'])
#     df['rank_pl'] = pd.Series(np.arange(df.shape[0]), index=df.index)

#     df = df.sort_values(by=['roe'], ascending=False)
#     df['rank_roe'] = pd.Series(np.arange(df.shape[0]), index=df.index)

#     df = get_tb_psbe(df)
#     df = df.sort_values(by=['upside'], ascending=False)
#     df['rank_psbe'] = pd.Series(np.arange(df.shape[0]), index=df.index)

#     df['rank'] = df['rank_pl'] + df['rank_roe'] + \
#         df['rank_graham'] + df['rank_psbe']
#     df = df.sort_values(by=['rank'], ascending=True)

#     return df


def get_tb_peg(tb):
    df = tb.copy()

    df = df[df['liquidez'] > LIQUIDEZ_THRESHOLD]
    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]

    if 'cagr' in df.columns.tolist():
        df['peg'] = df['p/l'] / df['cagr']
    else:
        df['peg'] = 0

    df = df[df['peg'] > 0]
    df['peg'] = df['peg'].round(4)

    df['empresa'] = df['ticker'].str[:4]

    df = df.sort_values(by=['peg'], ascending=True).reset_index()
    df = df.groupby(['empresa']).first().reset_index()
    df = df.sort_values(by=['peg'], ascending=True)

    df['peg'] = df['peg'].round(4)
    df['rank'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df = df.drop(columns=['empresa', 'index'])

    return df


def get_tb_bazim(tb):
    df = tb.copy()

    df = df[df['dy'] > 6]
    df = df[df['liquidez'] > LIQUIDEZ_THRESHOLD]
    df = df[df['div/pat'] < 3]

    df['desconto'] = df['p/l'] / 16.666
    df = df.sort_values(by=['desconto'], ascending=True)


    return df


def get_tb_ev_roic(tb):
    df = tb.copy()

    df = df[df['liquidez'] > LIQUIDEZ_THRESHOLD]
    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]
    if 'ev/ebitda' in df:
        df = df[df['ev/ebitda'] >= 0]
        df = df.sort_values(by=['ev/ebitda'])

    if 'ev/ebit' in df:
        df = df[df['ev/ebit'] >= 0]
        df = df.sort_values(by=['ev/ebit'])

    df['rank_ev'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df = df.sort_values(by=['roic'], ascending=False)
    df['rank_roic'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df['rank_ev_roic'] = df['rank_ev'] + df['rank_roic']
    df = df.sort_values(by=['rank_ev_roic'])

    df['rank'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    return df


def get_tb_psbe(tb):
    df = tb.copy()

    df = df[df['liquidez'] > LIQUIDEZ_THRESHOLD]
    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]
    # df = df[df['dy'] > 0]
    df = df[df['roe'] > TAXA_SELIC]
    df = df[df['cagr'] > -5]
    if 'ev/ebitda' in df:
        df = df[df['ev/ebitda'] >= 0]
    if 'ev/ebit' in df:
        df = df[df['ev/ebit'] >= 0]

    # df = df.sort_values(by=['ev/ebitda'])
    # df['rank_ev'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    # df = df.sort_values(by=['roic'], ascending=False)
    # df['rank_roic'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    # df['rank_ev_roic'] = df['rank_ev'] + df['rank_roic']
    # df = df.sort_values(by=['rank_ev_roic'])

    # tabela SI
    if 'patrimonio' not in df:
        df['patrimonio'] = df['preco'] / df['p/vp']

    df['ll'] = (df['roe']/100) * df['patrimonio']
    df['rl'] = df['ll'] / (df['margemLiquida']/100)
    df['n'] = df['ll'] * df['p/l'] / df['preco']
    df['vm'] = df['n'] * df['preco']
    cte = 7
    # cte = 5.891

    margem_seguranca = .25
    df['psbe'] = (df['patrimonio'] + df['rl'] + df['ll'] * np.exp((df['margemLiquida']/100)
                                                                  * -1 * np.log(np.abs(df['margemLiquida']/100)) * cte * np.sign(df['margemLiquida']))) / df['n']
    df['ms'] = df['psbe'] * (1 - margem_seguranca)
    df['upside'] = 100 * ((df['ms'] / df['preco']) - 1)

    df['psbe'] = df['psbe'].round(2)
    df['ms'] = df['ms'].round(2)
    df['upside'] = df['upside'].round(2)

    df['empresa'] = df['ticker'].str[:4]

    df = df.sort_values(by=['upside'], ascending=False).reset_index()
    df = df.groupby(['empresa']).first().reset_index()

    df = df.sort_values(by=['upside'], ascending=False)
    df = df.drop(columns=['ll', 'rl', 'n', 'vm', 'empresa', 'index'])

    df['rank'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    return df


def get_tb_fcd(tb):
    df = tb.copy()

    df = df[df['liquidez'] > LIQUIDEZ_THRESHOLD]
    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]
    df = df[df['roe'] > 5]
    df = df[df['cagr'] > -5]
    if 'ev/ebitda' in df:
        df = df[df['ev/ebitda'] >= 0]
    if 'ev/ebit' in df:
        df = df[df['ev/ebit'] >= 0]

    df['lpa'] = df['preco'] / df['p/l']
    tx_desconto = .09
    tx_perpetuidade = .03
    delta = tx_desconto - tx_perpetuidade

    tx_crescimento = df['cagr']/100
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

    df['ms'] = df['preco_ano_5'] * (1 - MARGEM_SEGURANCA)
    df['upside'] = 100 * ((df['ms'] / df['preco']) - 1)

    df['lpa'] = df['lpa'].round(2)
    df['preco_ano_1'] = df['preco_ano_1'].round(2)
    df['preco_ano_2'] = df['preco_ano_2'].round(2)
    df['preco_ano_3'] = df['preco_ano_3'].round(2)
    df['preco_ano_4'] = df['preco_ano_4'].round(2)
    df['preco_ano_5'] = df['preco_ano_5'].round(2)
    df['ms'] = df['ms'].round(2)
    df['upside'] = df['upside'].round(2)

    df['empresa'] = df['ticker'].str[:4]

    df = df.sort_values(by=['upside'], ascending=False).reset_index()
    df = df.groupby(['empresa']).first().reset_index()
    df = df.sort_values(by=['upside'], ascending=False)

    df['rank'] = pd.Series(np.arange(df.shape[0]), index=df.index)

    df = df.drop(columns=['empresa', 'index'])

    return df


def get_tb_psbe_geral(tb):
    df = tb.copy()

    df = df[df['liquidez'] > LIQUIDEZ_THRESHOLD]
    df = df[df['p/l'] > 0]
    df = df[df['p/vp'] > 0]

    df['ll'] = (df['roe']/100) * df['patrimonio']
    df['rl'] = df['ll'] / (df['margemLiquida']/100)
    df['n'] = df['ll'] * df['p/l'] / df['preco']
    df['vm'] = df['n'] * df['preco']
    cte = 7
    # cte = 5.891

    margem_seguranca = .25
    df['psbe'] = (df['patrimonio'] + df['rl'] + df['ll'] * np.exp((df['margemLiquida']/100)
                                                                  * -1 * np.log(np.abs(df['margemLiquida']/100)) * cte * np.sign(df['margemLiquida']))) / df['n']
    df['ms'] = df['psbe'] * (1 - margem_seguranca)
    df['upside'] = 100 * ((df['ms'] / df['preco']) - 1)

    df['psbe'] = df['psbe'].round(2)
    df['ms'] = df['ms'].round(2)
    df['upside'] = df['upside'].round(2)

    df['empresa'] = df['ticker'].str[:4]

    df = df.sort_values(by=['upside'], ascending=False).reset_index()
    df = df.groupby(['empresa']).first().reset_index()

    df = df.sort_values(by=['upside'], ascending=False)
    df = df.drop(columns=['ll', 'rl', 'n', 'vm', 'empresa', 'index'])

    return df
