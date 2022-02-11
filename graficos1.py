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

# Mostrar el mercado a partir de dataframe con formato Epoch

df = pd.DataFrame(bars[:-1], columns=['time', 'open', 'high', 'low', 'close', 'volume'])
#print(df)
x = [1, 4, 5, 6]
plt.plot(df.time, df.close)
plt.show()

# Intento de pasar de Epoch a Datetime

# m[0]=datetime.datetime.fromtimestamp(int(str(m[0]).rstrip("0")+"0"))
# epoch_time = 1644399060000
# epoch_time=int(str(epoch_time).rstrip("0")+"0")
# time_val = datetime.datetime.fromtimestamp(epoch_time)
# print('Date:', time_val)


bars = exchange.fetch_ohlcv('XBTUSD', timeframe='1m', limit=13)

# pasar de Epoch a Datetime

for m in bars:
    fecha = datetime.datetime.fromtimestamp(m[0] / 1000)
    hora = str(fecha.hour) + ":" + str(fecha.minute)
    m[0] = hora

# Mostrar el mercado a partir de dataframe

df = pd.DataFrame(bars[:-1], columns=['time', 'open', 'high', 'low', 'close', 'volume'])
print(df)
x = [1, 4, 5, 6]
plt.plot(df.time, df.close)
plt.show()

"""
def send_order(data):

    This function sends the order to the exchange using ccxt.
    :param data: python dict, with keys as the API parameters.
    :return: the response from the exchange.
    

    # Replace kraken with your exchange of choice.
    exchange = ccxt.bitmex({
        # Inset your API key and secrets for exchange in question.
        'apiKey': 'ZSGFq...........',
        'secret': 'IgqmKF................',
        'enableRateLimit': True,
    })

    # alper: Bitmex testnet url:
    if 'test' in exchange.urls:
        exchange.urls['api'] = exchange.urls['test'] # ←----- switch the base URL to testnet
    print(exchange.fetch_balance())
"""
