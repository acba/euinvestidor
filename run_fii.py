import os

import pandas as pd
import numpy as np
import requests
import bs4

import utils.fiis.misc as fii
import utils.misc as misc

tb_fiis = fii.get_table_fiis()
tb_fs = fii.get_table_funds_explorer()

tb_fii = tb_fs.merge(tb_fiis, on='papel', how='left', suffixes=('', '_y'))
tb_fii = tb_fii.drop(columns=['preco_y', 'dy_y', 'dy12m_y', 'p/vpa_y', 'liquidez_y'])

nome = f'analise_fii.xlsx'
out = misc.cria_tabela(nome)

tb_upside = fii.get_tb_upside(tb_fii)
tb_pvpa_rent = fii.get_tb_pvpa_rent(tb_fii)
tb_pvpa_dy12m = fii.get_tb_pvpa_dy12m(tb_fii)
tb_pvpa_dy6m_adj = fii.get_tb_pvpa_dy6m_adj(tb_fii)


misc.add_planilha(out, 'geral', tb_fii)
misc.add_planilha(out, 'upside', tb_upside)
misc.add_planilha(out, 'tb_pvpa_rent', tb_pvpa_rent)
misc.add_planilha(out, 'tb_pvpa_dy12m', tb_pvpa_dy12m)
misc.add_planilha(out, 'tb_pvpa_dy6m_adj', tb_pvpa_dy6m_adj)

misc.salva_tabela(out)
