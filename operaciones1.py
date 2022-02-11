import ccxt
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
import request
import datetime
import time

exchange = ccxt.bitmex({
    'apiKey': 'upVhyYASwSu7nJTMRayZY7lD',
    'secret': 'eo8iXfn2Lp17RPKf3MN5WeUB5q9MeAvR3dbxuEVPfdGNL1WH',
})
if 'test' in exchange.urls:
    exchange.urls['api'] = exchange.urls['test']  # ←----- switch the base URL to testnet
#print(exchange.fetch_balance())
bars = exchange.fetch_ohlcv('XBTUSD', timeframe='1m', limit=1000)
exchange.set_sandbox_mode(True)

if exchange.has['createMarketOrder']:
    exchange.createOrder('XBTUSD', 'market', 'buy', 100, ...)

# Historial de transacciones con órdenes Python
# Orden de venta market ejecutada en 44388        LOSE
# Orden de compra market ejecutada en 44417.5

# Orden de compra market ejecutada en 44452.5     WIN
# Orden de venta market ejecutada en 44477.5

# Orden de compra market ejecutada en 44497.5   WIN
# Orden de venta market ejecutada en 44529.5

