# encoding=utf8
import os

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

import requests
import ipdb

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def exponenial_func(x, a, b, c):
    return a*np.exp(-b*x)+c

dividendos = [
  0, 22.6, 76.3,
  140, 152.1, 204.4,
  177.4, 134.2, 285.8,
  157.7, 121.8, 236.5, 
  168.9, 190, 301.2,
  608.2, 145.5, 274.1,
  276.5, 337.2
]

x = np.arange(len(dividendos))
fx = dividendos

fit1d = np.poly1d(np.polyfit(x, fx, deg=1))
fit2d = np.poly1d(np.polyfit(x, fx, deg=2))
fit3d = np.poly1d(np.polyfit(x, fx, deg=3))
fit4d = np.poly1d(np.polyfit(x, fx, deg=4))

popt, pcov = curve_fit(exponenial_func, x, fx)

x_date = np.arange('2017-12', '2023-01', dtype='datetime64[M]')

x = np.arange(len(x_date))
y1d = fit1d(x)
y2d = fit2d(x)
y3d = fit3d(x)
y4d = fit4d(x)
exp = exponenial_func(x, *popt)

div = np.concatenate((dividendos, np.zeros(len(x) - len(dividendos))))

mmtrimestre = np.concatenate((np.zeros(2), moving_average(dividendos), np.zeros(len(x) - len(dividendos)) ))
mmsemestre = np.concatenate((np.zeros(5), moving_average(dividendos, 6), np.zeros(len(x) - len(dividendos)) ))


fig, ax = plt.subplots()
line1, = ax.plot(x_date, div, label='Dividendos')
line1, = ax.plot(x_date, y1d, label='Fit 1D')
# line1, = ax.plot(x_date, y2d, label='Fit 2D')
# line1, = ax.plot(x_date, exp, label='Exp')
line1, = ax.plot(x_date, mmtrimestre, label='Média Móvel 3t')
line1, = ax.plot(x_date, mmsemestre, label='Média Móvel 6t')
# line1, = ax.plot(x_date, y3d, label='Fit 3D')
# line1, = ax.plot(x_date, y4d, label='Fit 4D')

ax.legend()
plt.show()

