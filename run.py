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

misc.calcula_planilhas(out, tb_fundamentus, 'fundamentus', 'f_')
misc.calcula_planilhas(out, tb_si, 'statusinvest', 'si_')

# misc.add_planilha(out, 'fundamentus', tb_fundamentus)

# misc.add_planilha(out, 'f_graham', misc.get_tb_num_graham_puro(tb_fundamentus))
# misc.add_planilha(out, 'f_graham_rentaveis', misc.get_tb_num_graham_rentaveis(tb_fundamentus))
# misc.add_planilha(out, 'f_graham_ajustado', misc.get_tb_graham_ajustado(tb_fundamentus))
# misc.add_planilha(out, 'f_peg', misc.get_tb_peg(tb_fundamentus))
# misc.add_planilha(out, 'f_ev_roic', misc.get_tb_ev_roic(tb_fundamentus))
# misc.add_planilha(out, 'f_psbe', misc.get_tb_psbe(tb_fundamentus))
# misc.add_planilha(out, 'f_fcd', misc.get_tb_fcd(tb_fundamentus))

# Status Invest

# misc.add_planilha(out, 'statusinvest', tb_si)

# misc.add_planilha(out, 'si_graham', misc.get_tb_num_graham_puro(tb_si))
# misc.add_planilha(out, 'si_graham_rentaveis', misc.get_tb_num_graham_rentaveis(tb_si))
# misc.add_planilha(out, 'si_graham_ajustado', misc.get_tb_graham_ajustado(tb_si))
# misc.add_planilha(out, 'si_peg', misc.get_tb_peg(tb_si))
# misc.add_planilha(out, 'si_ev_roic', misc.get_tb_ev_roic(tb_si))
# misc.add_planilha(out, 'si_psbe', misc.get_tb_psbe(tb_si))
# misc.add_planilha(out, 'si_fcd', misc.get_tb_fcd(tb_si))

misc.salva_tabela(out)

# tb_graham.to_html('graham.html')
