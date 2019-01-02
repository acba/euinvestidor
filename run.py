# encoding=utf8

import pandas as pd
import numpy as np
import requests

tipo_analise = 'geral'

headers = {
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

analise = {
    'geral': '',
    'Petróleo, Gás e Biocombustíveis': '1',
    'Mineração': '2',
    'Previdência e Seguros': '38',
    'Alimentos': '15',
    'bancos': '35',
    'eletricas': '32',
}

writer = pd.ExcelWriter('dados/analise_{}.xlsx'.format(tipo_analise))
if tipo_analise == 'geral':
    url = 'http://www.fundamentus.com.br/resultado.php'
else:
    url = 'http://www.fundamentus.com.br/resultado.php?setor={}'.format(analise[tipo_analise])

response = requests.get(url, headers=headers)
tb = pd.read_html(response.text, decimal=",", thousands=".")[0]

# Tratando dados
tb['Div.Yield']     = pd.to_numeric(tb['Div.Yield'].str.replace('.', '').str.replace('%','').str.replace(',','.'))
tb['Mrg Ebit']      = pd.to_numeric(tb['Mrg Ebit'].str.replace('.', '').str.replace('%','').str.replace(',','.'))
tb['Mrg. Líq.']     = pd.to_numeric(tb['Mrg. Líq.'].str.replace('.', '').str.replace('%','').str.replace(',','.'))
tb['ROIC']          = pd.to_numeric(tb['ROIC'].str.replace('.', '').str.replace('%','').str.replace(',','.'))
tb['ROE']           = pd.to_numeric(tb['ROE'].str.replace('.', '').str.replace('%','').str.replace(',','.'))
tb['Cresc. Rec.5a'] = pd.to_numeric(tb['Cresc. Rec.5a'].str.replace('.', '').str.replace('%','').str.replace(',','.'))

# Calculos intermediarios
tb['BUFF']    = tb['P/L'] * tb['P/VP']
tb['PEG']     = tb['P/L'] / (tb['Cresc. Rec.5a'])
tb['PEG_ADJ'] = tb['P/L'] / (tb['Cresc. Rec.5a'] + tb['Div.Yield'])
tb['PED']     = tb['P/L'] / (tb['Div.Yield'])

tb['BUFF_EV']    = tb['EV/EBIT'] * tb['P/VP']
tb['PEG_EV']     = tb['EV/EBIT'] / (tb['Cresc. Rec.5a'])
tb['PEG_ADJ_EV'] = tb['EV/EBIT'] / (tb['Cresc. Rec.5a'] + tb['Div.Yield'])
tb['PED_EV']     = tb['EV/EBIT'] / (tb['Div.Yield'])

tb.to_excel(writer, 'planilha')

# Apenas acoes com liquidez
tb = tb.loc[tb['Liq.2meses'] > 50000]


##
## ANALISE DIV YIELD
##

div = tb.loc[tb['Div.Yield'] > 3]
div.sort_values(by=['Div.Yield'], ascending=False).to_excel(writer, 'div_yield')

##
## ANALISE PEG
##

tb_peg = tb.copy()
tb_peg = tb_peg.loc[tb_peg['P/L'] > 0]
tb_peg = tb_peg.loc[tb_peg['Cresc. Rec.5a'] > 0]
tb_peg = tb_peg.sort_values(by=['PEG'])
tb_peg['rank_peg'] = pd.Series(np.arange(tb_peg.shape[0]), index=tb_peg.index)
tb_peg.to_excel(writer, 'peg')

##
## ANALISE PEG_ADJ
##

tb_peg = tb.copy()
tb_peg = tb_peg.loc[tb_peg['P/L'] > 0]
tb_peg = tb_peg.loc[tb_peg['Cresc. Rec.5a'] > 0]
tb_peg = tb_peg.loc[tb_peg['Div.Yield'] > 0]
tb_peg = tb_peg.sort_values(by=['PEG_ADJ'])
tb_peg['rank_peg_adj'] = pd.Series(np.arange(tb_peg.shape[0]), index=tb_peg.index)
tb_peg.to_excel(writer, 'peg_adj')

##
## ANALISE EV/EBIT -> ROIC
##

tb_ev_roic = tb.copy()
tb_ev_roic = tb_ev_roic.loc[ tb_ev_roic['EV/EBIT'] > 0 ]


tb_ev_roic = tb_ev_roic.sort_values(by=['EV/EBIT'])
tb_ev_roic['rank_ev'] = pd.Series(np.arange(tb_ev_roic.shape[0]), index=tb_ev_roic.index)

tb_ev_roic = tb_ev_roic.sort_values(by=['ROIC'], ascending=False)
tb_ev_roic['rank_roic'] = pd.Series(np.arange(tb_ev_roic.shape[0]), index=tb_ev_roic.index)

tb_ev_roic['rank_ev_roic'] = tb_ev_roic['rank_ev'] + tb_ev_roic['rank_roic']
tb_ev_roic=tb_ev_roic.sort_values(by=['rank_ev_roic'])

tb_ev_roic.to_excel(writer,'ev_roic')

##
## ANALISE EV/EBIT -> ROE
##

data = tb.copy()
data = data.loc[ data['EV/EBIT'] > 0 ]


data = data.sort_values(by=['EV/EBIT'])
data['rank_ev'] = pd.Series(np.arange(data.shape[0]), index=data.index)

data = data.sort_values(by=['ROE'], ascending=False)
data['rank_roe'] = pd.Series(np.arange(data.shape[0]), index=data.index)

data['rank_ev_roe'] = data['rank_ev'] + data['rank_roe']
data=data.sort_values(by=['rank_ev_roe'])

data.to_excel(writer,'ev_roe')

##
## ANALISE P/L -> ROIC
##

tb_pl_roic = tb.copy()
tb_pl_roic = tb_pl_roic.loc[ tb_pl_roic['P/L'] > 0 ]

tb_pl_roic = tb_pl_roic.sort_values(by=['P/L'])
tb_pl_roic['rank_pl'] = pd.Series(np.arange(tb_pl_roic.shape[0]), index=tb_pl_roic.index)

tb_pl_roic = tb_pl_roic.sort_values(by=['ROIC'], ascending=False)
tb_pl_roic['rank_roic'] = pd.Series(np.arange(tb_pl_roic.shape[0]), index=tb_pl_roic.index)

tb_pl_roic['rank_pl_roic'] = tb_pl_roic['rank_pl'] + tb_pl_roic['rank_roic']
tb_pl_roic=tb_pl_roic.sort_values(by=['rank_pl_roic'])

tb_pl_roic.to_excel(writer,'pl_roic')


##
## ANALISE P/L -> ROE
##

tb_pl_roe = tb.copy()
tb_pl_roe = tb_pl_roe.loc[ tb_pl_roe['P/L'] > 0 ]

tb_pl_roe = tb_pl_roe.sort_values(by=['P/L'])
tb_pl_roe['rank_pl'] = pd.Series(np.arange(tb_pl_roe.shape[0]), index=tb_pl_roe.index)

tb_pl_roe = tb_pl_roe.sort_values(by=['ROE'], ascending=False)
tb_pl_roe['rank_roe'] = pd.Series(np.arange(tb_pl_roe.shape[0]), index=tb_pl_roe.index)

tb_pl_roe['rank_pl_roe'] = tb_pl_roe['rank_pl'] + tb_pl_roe['rank_roe']
tb_pl_roe=tb_pl_roe.sort_values(by=['rank_pl_roe'])

tb_pl_roe.to_excel(writer,'pl_roe')


##
## ANALISE FORMULA MAGICA + WARREN BUFFET LIMIT -> EV/EBIT -> ROIC
##

tb_pl_roic = tb.copy()
tb_pl_roic = tb_pl_roic.loc[tb_pl_roic['P/L'] > 0]
tb_pl_roic = tb_pl_roic.loc[tb_pl_roic['EV/EBIT'] > 0]

tb_pl_roic_wb = tb_pl_roic.loc[tb_pl_roic['P/L'] * tb_pl_roic['P/VP'] < 22.5]

tb_pl_roic_wb = tb_pl_roic_wb.sort_values(by=['EV/EBIT'])
tb_pl_roic_wb['rank_ev'] = pd.Series(np.arange(tb_pl_roic_wb.shape[0]), index=tb_pl_roic_wb.index)

tb_pl_roic_wb = tb_pl_roic_wb.sort_values(by=['ROIC'], ascending=False)
tb_pl_roic_wb['rank_roic'] = pd.Series(np.arange(tb_pl_roic_wb.shape[0]), index=tb_pl_roic_wb.index)

tb_pl_roic_wb['rank_ev_roic'] = tb_pl_roic_wb['rank_ev'] + tb_pl_roic_wb['rank_roic']
tb_pl_roic_wb=tb_pl_roic_wb.sort_values(by=['rank_ev_roic'])

tb_pl_roic_wb.to_excel(writer,'ev_roic_baratos')

writer.save()

##
## ANALISE FORMULA MAGICA + WARREN BUFFET LIMIT -> P/L -> ROE
##

tb_pl_roe_wb = tb_pl_roic.loc[tb_pl_roic['P/L'] * tb_pl_roic['P/VP'] < 22.5]

tb_pl_roe_wb = tb_pl_roe_wb.sort_values(by=['P/L'])
tb_pl_roe_wb['rank_pl'] = pd.Series(np.arange(tb_pl_roe_wb.shape[0]), index=tb_pl_roe_wb.index)

tb_pl_roe_wb = tb_pl_roe_wb.sort_values(by=['ROE'], ascending=False)
tb_pl_roe_wb['rank_roe'] = pd.Series(np.arange(tb_pl_roe_wb.shape[0]), index=tb_pl_roe_wb.index)

tb_pl_roe_wb['rank_pl_roe'] = tb_pl_roe_wb['rank_pl'] + tb_pl_roe_wb['rank_roe']
tb_pl_roe_wb=tb_pl_roe_wb.sort_values(by=['rank_pl_roe'])

tb_pl_roe_wb.to_excel(writer,'pl_roe_baratos')

writer.save()
