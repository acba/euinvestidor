import pandas as pd
import pandas_datareader.data as web

import datetime

start = datetime.datetime(2021,1,1)
end = datetime.datetime(2021,4,1)

precos = pd.DataFrame()
carteira = ['GOLD11.SA', 'BOVA11.SA', 'IVVB11.SA', 'SMAL11.SA', 'VNQ']

for ticker in carteira:
    precos[ticker] = web.DataReader(ticker, data_source='yahoo', start=start, end=end)['Adj Close']

retornos = precos/precos.shift(1) - 1

print(precos.head())
print(retornos.head())

print(retornos.mean())
print(retornos.std())
