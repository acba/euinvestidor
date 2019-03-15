import os
from pathlib import Path

import pandas as pd
import numpy as np
import ipdb


def cria_tabela(filename):
    _cria_outdir()
    path = Path(_get_outdir())
    fullpath = path / filename

    return pd.ExcelWriter(str(fullpath))

def add_planilha(writer, nome_planilha, tb):
    tb.to_excel(writer, nome_planilha, index=False)


def salva_tabela(writer):
    writer.save()


def _get_outdir():
    return './dados/'


def _cria_outdir():
    path = _get_outdir()
    if not os.path.exists(path):
        os.makedirs(path)
