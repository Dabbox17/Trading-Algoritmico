import ccxt
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
import request
import datetime
import time

#Este algoritmo funciona con entradas market y realiza
# compra/venta cuando la EMA10 y la EMA5 se intersectan en cualquiera de las dos
#direcciones
#Imprecisiones

exchange = ccxt.bitmex({
    'apiKey': '',
    'secret': '',
})
if 'test' in exchange.urls:
    exchange.urls['api'] = exchange.urls['test']  # ←----- switch the base URL to testnet
exchange.set_sandbox_mode(True)

invertido=False
corto=False
largo=False

while True:
    bars = exchange.fetch_ohlcv('XBTUSD', timeframe='1m', limit=30)
    df = pd.DataFrame(bars[:-1], columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    datos = df.close.tolist()

    time.sleep(60)
    SMA30= round(mean(datos[len(datos) - 30:len(datos)]))
    SMA5 = round(mean(datos[len(datos) -5 :len(datos)]))
    print("SMA30:",SMA30)
    print("SMA5:",SMA5)

    if invertido:
        if SMA30 > SMA5 and largo:
            exchange.createOrder('XBTUSD', 'market', 'sell', 100, ...)
            largo=False
            print("Largo:",largo)
            print("Corto:",corto)

        if SMA30 < SMA5 and corto:
            exchange.createOrder('XBTUSD', 'market', 'buy', 100, ...)
            corto=False
            print("Largo:", largo)
            print("Corto:", corto)

    else:
        if SMA30 > SMA5:
            exchange.createOrder('XBTUSD', 'market', 'buy', 100, ...)
            largo=True
            invertido=True
            print("Largo:", largo)
            print("Corto:", corto)

        elif SMA30 < SMA5:
            exchange.createOrder('XBTUSD', 'market', 'sell', 100, ...)
            corto=True
            invertido=True
            print("Largo:", largo)
            print("Corto:", corto)
