import os

import pandas as pd
import numpy as np
import requests

import utils.misc as misc

url = 'https://fiis.com.br/filtro'
response = requests.get(url)


# fetch("https://fiis.com.br/filtro", {
#     "credentials": "include", 
#     "headers": {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", "accept-language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7", "cache-control": "no-cache", "content-type": "application/x-www-form-urlencoded", "pragma": "no-cache", "upgrade-insecure-requests": "1"}, 
#     "referrer": "https://fiis.com.br/filtro/", 
#     "referrerPolicy": "no-referrer-when-downgrade",
#     "body": "exnome=on&exmercado=on&flmercadobolsa=on&flmercadobalcao=on&expublico=on&flpublicogeral=on&flpublicoiq=on&extipo=on&fltipo16=on&fltipo10=on&fltipo12=on&fltipo2=on&fltipo15=on&fltipo5=on&fltipo1=on&fltipo14=on&fltipo6=on&fltipo9=on&fltipo11=on&fltipo3=on&fltipo4=on&fltipo7=on&fltipo13=on&fltipo8=on&exadm=on&fladm1=on&fladm2=on&fladm39=on&fladm3=on&fladm33=on&fladm32=on&fladm4=on&fladm5=on&fladm6=on&fladm7=on&fladm8=on&fladm9=on&fladm10=on&fladm11=on&fladm31=on&fladm12=on&fladm13=on&fladm14=on&fladm0=on&fladm15=on&fladm16=on&fladm38=on&fladm17=on&fladm28=on&fladm18=on&fladm19=on&fladm20=on&fladm35=on&fladm30=on&fladm21=on&fladm37=on&fladm22=on&fladm29=on&fladm23=on&fladm24=on&fladm36=on&fladm25=on&fladm34=on&fladm26=on&fladm27=on&exfechamento=on&exurendrs=on&exurendper=on&urendpermin=&urendpermax=&exdatapag=on&exdatabase=on&exrendmedrs=on&exrendmedper=on&rendmedpermin=&rendmedpermax=&exppc=on&expvp=on&pvpmin=&pvpmax=&exnneg=on&nnegmin=&txpl=on&txrec=on&txvm=on&txvs=on&txrs=on&ordenapor=codneg&ordena1=ASC", 
#     "method": "POST", 
#     "mode": "cors"})
