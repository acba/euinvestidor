# encoding=utf8
import os

import pandas as pd
import numpy as np
import requests

import utils.acoes.misc as misc


setor_analise = 'geral'

url = misc.get_url(setor_analise)
tb_geral = misc.get_table(url)

nome = f'analise_{setor_analise}.xlsx'
out = misc.cria_tabela(nome)

tb_graham_puro  = misc.get_tb_num_graham_puro(tb_geral)
tb_graham       = misc.get_tb_num_graham(tb_geral)
# tb_graham2      = misc.get_tb_num_graham2(tb_geral)
# tb_graham3      = misc.get_tb_num_graham3(tb_geral)
tb_peg          = misc.get_tb_peg(tb_geral)
tb_bazim        = misc.get_tb_bazim(tb_geral)
tb_ev_roic      = misc.get_tb_ev_roic(tb_geral)
tb_psbe         = misc.get_tb_psbe(tb_geral)
tb_composto         = misc.get_tb_composta(tb_geral)

misc.add_planilha(out, 'geral', tb_geral)
misc.add_planilha(out, 'tb_graham_puro', tb_graham_puro)
misc.add_planilha(out, 'graham', tb_graham)
# misc.add_planilha(out, 'graham2', tb_graham2)
# misc.add_planilha(out, 'graham3', tb_graham3)
misc.add_planilha(out, 'peg', tb_peg)
misc.add_planilha(out, 'bazim', tb_bazim)
misc.add_planilha(out, 'ev_roic', tb_ev_roic)
misc.add_planilha(out, 'psbe', tb_psbe)
misc.add_planilha(out, 'composto', tb_composto)

misc.salva_tabela(out)

# tb_graham.to_html('graham.html')
