# encoding=utf8
import os

import pandas as pd
import numpy as np
import requests

import utils.acoes.misc as misc
from utils.acoes.misc import Fontes

setor = 'geral'
tb_fundamentus = misc.get_table(setor, fonte=Fontes.FUNDAMENTUS)
tb_si = misc.get_table(setor, fonte=Fontes.STATUSINVEST)

nome = f'analise_{setor}.xlsx'
out = misc.cria_tabela(nome)

# tb_graham_limpo = misc.get_tb_num_graham_limpa(tb_geral)
# tb_graham_ajustado       = misc.get_tb_graham_ajustado(tb_geral)
# # tb_graham2      = misc.get_tb_num_graham2(tb_geral)
# # tb_graham3      = misc.get_tb_num_graham3(tb_geral)
# tb_peg          = misc.get_tb_peg(tb_geral)
# tb_bazim        = misc.get_tb_bazim(tb_geral)
# tb_ev_roic      = misc.get_tb_ev_roic(tb_geral)
# tb_psbe         = misc.get_tb_psbe(tb_geral)
# tb_psbe_geral   = misc.get_tb_psbe_geral(tb_geral)
# tb_fcd          = misc.get_tb_fcd(tb_geral)
# tb_composto     = misc.get_tb_composta(tb_geral)

misc.add_planilha(out, 'fundamentus', tb_fundamentus)
misc.add_planilha(out, 'statusinvest', tb_si)

misc.add_planilha(out, 'f_graham', misc.get_tb_num_graham_puro(tb_fundamentus))
# misc.add_planilha(out, 'tb_graham_puro', tb_graham_puro)
# misc.add_planilha(out, 'tb_graham_limpo', tb_graham_limpo)
# misc.add_planilha(out, 'graham_ajustado', tb_graham_ajustado)
# # misc.add_planilha(out, 'graham2', tb_graham2)
# # misc.add_planilha(out, 'graham3', tb_graham3)
# misc.add_planilha(out, 'peg', tb_peg)
# misc.add_planilha(out, 'bazim', tb_bazim)
# misc.add_planilha(out, 'ev_roic', tb_ev_roic)
# misc.add_planilha(out, 'psbe', tb_psbe)
# misc.add_planilha(out, 'psbe_geral', tb_psbe_geral)
# misc.add_planilha(out, 'fcd', tb_fcd)
# misc.add_planilha(out, 'composto', tb_composto)

# Status Invest

misc.add_planilha(out, 'si_graham', misc.get_tb_num_graham_puro(tb_si))

misc.salva_tabela(out)

# tb_graham.to_html('graham.html')
