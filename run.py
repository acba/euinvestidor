# encoding=utf8
import os

import pandas as pd
import numpy as np
import requests

import utils.misc as misc


setor_analise = 'geral'

url = misc.get_url(setor_analise)
tb_geral = misc.get_table(url)

nome = f'analise_{setor_analise}.xlsx'
out = misc.cria_tabela(nome)

tb_graham  = misc.get_tb_num_graham(tb_geral)
tb_graham2 = misc.get_tb_num_graham2(tb_geral)
tb_graham3 = misc.get_tb_num_graham3(tb_geral)
tb_peg     = misc.get_tb_peg(tb_geral)
tb_bazim   = misc.get_tb_bazim(tb_geral)
tb_ev_roic = misc.get_tb_ev_roic(tb_geral)

misc.add_planilha(out, 'geral', tb_geral)
misc.add_planilha(out, 'graham', tb_graham)
misc.add_planilha(out, 'graham2', tb_graham2)
misc.add_planilha(out, 'graham3', tb_graham3)
misc.add_planilha(out, 'peg', tb_peg)
misc.add_planilha(out, 'bazim', tb_bazim)
misc.add_planilha(out, 'ev_roic', tb_ev_roic)

misc.salva_tabela(out)

tb_graham.to_html('graham.html')

# Calculos intermediarios
# tb['BUFF']    = tb['P/L'] * tb['P/VP']
# tb['PEG']     = tb['P/L'] / (tb['Cresc. Rec.5a'])
# tb['PEG_ADJ'] = tb['P/L'] / (tb['Cresc. Rec.5a'] + tb['Div.Yield'])
# tb['PED']     = tb['P/L'] / (tb['Div.Yield'])

# tb['BUFF_EV']    = tb['EV/EBIT'] * tb['P/VP']
# tb['PEG_EV']     = tb['EV/EBIT'] / (tb['Cresc. Rec.5a'])
# tb['PEG_ADJ_EV'] = tb['EV/EBIT'] / (tb['Cresc. Rec.5a'] + tb['Div.Yield'])
# tb['PED_EV']     = tb['EV/EBIT'] / (tb['Div.Yield'])

# tb.to_excel(writer, 'planilha', index=False)

# # Apenas acoes com liquidez
# tb = tb.loc[tb['Liq.2meses'] > 50000]


# ##
# ## ANALISE DIV YIELD
# ##

# div = tb.loc[tb['Div.Yield'] > 3]
# div.sort_values(by=['Div.Yield'], ascending=False).to_excel(writer, 'div_yield', index=False)


# ##
# ## ANALISE DIV YIELD EV_ROIC
# ##

# div = tb.copy()
# div = div.loc[div['Div.Yield'] > 0]
# div = div.loc[div['EV/EBIT'] > 0]


# div = div.sort_values(by=['EV/EBIT'])
# div['rank_ev'] = pd.Series(np.arange(div.shape[0]), index=div.index)

# div = div.sort_values(by=['ROIC'], ascending=False)
# div['rank_roic'] = pd.Series(np.arange(div.shape[0]), index=div.index)

# div['rank_ev_roic'] = div['rank_ev'] + div['rank_roic']
# div = div.sort_values(by=['rank_ev_roic'])

# div.to_excel(writer, 'div_ev_roic', index=False)

# ##
# ## ANALISE PEG
# ##

# tb_peg = tb.copy()
# tb_peg = tb_peg.loc[tb_peg['P/L'] > 0]
# tb_peg = tb_peg.loc[tb_peg['Cresc. Rec.5a'] > 0]
# tb_peg = tb_peg.sort_values(by=['PEG'])
# tb_peg['rank_peg'] = pd.Series(np.arange(tb_peg.shape[0]), index=tb_peg.index)
# tb_peg.to_excel(writer, 'peg', index=False)

# ##
# ## ANALISE PEG_ADJ
# ##

# tb_peg = tb.copy()
# tb_peg = tb_peg.loc[tb_peg['P/L'] > 0]
# tb_peg = tb_peg.loc[tb_peg['Cresc. Rec.5a'] > 0]
# tb_peg = tb_peg.loc[tb_peg['Div.Yield'] > 0]
# tb_peg = tb_peg.sort_values(by=['PEG_ADJ'])
# tb_peg['rank_peg_adj'] = pd.Series(np.arange(tb_peg.shape[0]), index=tb_peg.index)
# tb_peg.to_excel(writer, 'peg_adj', index=False)

# ##
# ## ANALISE EV/EBIT -> ROIC
# ##

# tb_ev_roic = tb.copy()
# tb_ev_roic = tb_ev_roic.loc[ tb_ev_roic['EV/EBIT'] > 0 ]


# tb_ev_roic = tb_ev_roic.sort_values(by=['EV/EBIT'])
# tb_ev_roic['rank_ev'] = pd.Series(np.arange(tb_ev_roic.shape[0]), index=tb_ev_roic.index)

# tb_ev_roic = tb_ev_roic.sort_values(by=['ROIC'], ascending=False)
# tb_ev_roic['rank_roic'] = pd.Series(np.arange(tb_ev_roic.shape[0]), index=tb_ev_roic.index)

# tb_ev_roic['rank_ev_roic'] = tb_ev_roic['rank_ev'] + tb_ev_roic['rank_roic']
# tb_ev_roic=tb_ev_roic.sort_values(by=['rank_ev_roic'])

# tb_ev_roic.to_excel(writer, 'ev_roic', index=False)

# ##
# ## ANALISE EV/EBIT -> ROE
# ##

# data = tb.copy()
# data = data.loc[ data['EV/EBIT'] > 0 ]


# data = data.sort_values(by=['EV/EBIT'])
# data['rank_ev'] = pd.Series(np.arange(data.shape[0]), index=data.index)

# data = data.sort_values(by=['ROE'], ascending=False)
# data['rank_roe'] = pd.Series(np.arange(data.shape[0]), index=data.index)

# data['rank_ev_roe'] = data['rank_ev'] + data['rank_roe']
# data=data.sort_values(by=['rank_ev_roe'])

# data.to_excel(writer, 'ev_roe', index=False)

# ##
# ## ANALISE P/L -> ROIC
# ##

# tb_pl_roic = tb.copy()
# tb_pl_roic = tb_pl_roic.loc[ tb_pl_roic['P/L'] > 0 ]

# tb_pl_roic = tb_pl_roic.sort_values(by=['P/L'])
# tb_pl_roic['rank_pl'] = pd.Series(np.arange(tb_pl_roic.shape[0]), index=tb_pl_roic.index)

# tb_pl_roic = tb_pl_roic.sort_values(by=['ROIC'], ascending=False)
# tb_pl_roic['rank_roic'] = pd.Series(np.arange(tb_pl_roic.shape[0]), index=tb_pl_roic.index)

# tb_pl_roic['rank_pl_roic'] = tb_pl_roic['rank_pl'] + tb_pl_roic['rank_roic']
# tb_pl_roic=tb_pl_roic.sort_values(by=['rank_pl_roic'])

# tb_pl_roic.to_excel(writer, 'pl_roic', index=False)


# ##
# ## ANALISE P/L -> ROE
# ##

# tb_pl_roe = tb.copy()
# tb_pl_roe = tb_pl_roe.loc[ tb_pl_roe['P/L'] > 0 ]

# tb_pl_roe = tb_pl_roe.sort_values(by=['P/L'])
# tb_pl_roe['rank_pl'] = pd.Series(np.arange(tb_pl_roe.shape[0]), index=tb_pl_roe.index)

# tb_pl_roe = tb_pl_roe.sort_values(by=['ROE'], ascending=False)
# tb_pl_roe['rank_roe'] = pd.Series(np.arange(tb_pl_roe.shape[0]), index=tb_pl_roe.index)

# tb_pl_roe['rank_pl_roe'] = tb_pl_roe['rank_pl'] + tb_pl_roe['rank_roe']
# tb_pl_roe=tb_pl_roe.sort_values(by=['rank_pl_roe'])

# tb_pl_roe.to_excel(writer, 'pl_roe', index=False)


# ##
# ## ANALISE FORMULA MAGICA + WARREN BUFFET LIMIT -> EV/EBIT -> ROIC
# ##

# tb_pl_roic = tb.copy()
# tb_pl_roic = tb_pl_roic.loc[tb_pl_roic['P/L'] > 0]
# tb_pl_roic = tb_pl_roic.loc[tb_pl_roic['EV/EBIT'] > 0]

# tb_pl_roic_wb = tb_pl_roic.loc[tb_pl_roic['P/L'] * tb_pl_roic['P/VP'] < 22.5]

# tb_pl_roic_wb = tb_pl_roic_wb.sort_values(by=['EV/EBIT'])
# tb_pl_roic_wb['rank_ev'] = pd.Series(np.arange(tb_pl_roic_wb.shape[0]), index=tb_pl_roic_wb.index)

# tb_pl_roic_wb = tb_pl_roic_wb.sort_values(by=['ROIC'], ascending=False)
# tb_pl_roic_wb['rank_roic'] = pd.Series(np.arange(tb_pl_roic_wb.shape[0]), index=tb_pl_roic_wb.index)

# tb_pl_roic_wb['rank_ev_roic'] = tb_pl_roic_wb['rank_ev'] + tb_pl_roic_wb['rank_roic']
# tb_pl_roic_wb=tb_pl_roic_wb.sort_values(by=['rank_ev_roic'])

# tb_pl_roic_wb.to_excel(writer, 'ev_roic_baratos', index=False)

# writer.save()

# ##
# ## ANALISE FORMULA MAGICA + WARREN BUFFET LIMIT -> P/L -> ROE
# ##

# tb_pl_roe_wb = tb_pl_roic.loc[tb_pl_roic['P/L'] * tb_pl_roic['P/VP'] < 22.5]

# tb_pl_roe_wb = tb_pl_roe_wb.sort_values(by=['P/L'])
# tb_pl_roe_wb['rank_pl'] = pd.Series(np.arange(tb_pl_roe_wb.shape[0]), index=tb_pl_roe_wb.index)

# tb_pl_roe_wb = tb_pl_roe_wb.sort_values(by=['ROE'], ascending=False)
# tb_pl_roe_wb['rank_roe'] = pd.Series(np.arange(tb_pl_roe_wb.shape[0]), index=tb_pl_roe_wb.index)

# tb_pl_roe_wb['rank_pl_roe'] = tb_pl_roe_wb['rank_pl'] + tb_pl_roe_wb['rank_roe']
# tb_pl_roe_wb=tb_pl_roe_wb.sort_values(by=['rank_pl_roe'])

# tb_pl_roe_wb.to_excel(writer, 'pl_roe_baratos', index=False)

# writer.save()
