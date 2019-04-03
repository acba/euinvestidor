# encoding=utf8
import os

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import requests
import ipdb

dividendos = [
  0, 22.6, 76.3, 140, 152.1, 204.4, 177.4, 134.2,
  285.8, 157.7, 121.8, 236.5, 168.9, 190, 301.2, 523.7
]

coef = np.polyfit(np.arange(len(dividendos)), dividendos, deg=1)
fit1d = np.poly1d(coef)

coef = np.polyfit(np.arange(len(dividendos)), dividendos, deg=2)
fit2d = np.poly1d(coef)

coef = np.polyfit(np.arange(len(dividendos)), dividendos, deg=3)
fit3d = np.poly1d(coef)

coef = np.polyfit(np.arange(len(dividendos)), dividendos, deg=4)
fit4d = np.poly1d(coef)


x_date = np.arange('2017-12', '2023-01', dtype='datetime64[M]')
x = np.arange(len(x_date))
y1d = fit1d(x)
y2d = fit2d(x)
y3d = fit3d(x)
y4d = fit4d(x)
div = np.concatenate((dividendos, np.zeros(len(x) - len(dividendos))))


fig, ax = plt.subplots()
line1, = ax.plot(x_date, div, label='Dividendos')
line1, = ax.plot(x_date, y1d, label='Fit 1D')
line1, = ax.plot(x_date, y2d, label='Fit 2D')
# line1, = ax.plot(x_date, y3d, label='Fit 3D')
# line1, = ax.plot(x_date, y4d, label='Fit 4D')

ax.legend()
plt.show()

