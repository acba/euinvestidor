# encoding=utf8
import os

import pandas as pd
import numpy as np
import requests

import utils.misc as misc


path = './dados/'
if not os.path.exists(path):
    os.makedirs(path)

setor_analise = 'geral'

url = misc.get_url(setor_analise)
tb = misc.get_table(url)
