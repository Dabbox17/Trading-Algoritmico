import ccxt
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
import request
import datetime
import time
import mplfinance as mpf


#0:sell limit 1:buy limit 2:sell profit/loss  3:buy profit/loss

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
minutes=0
maximo=0
minimo=99999
siguientemax=False
siguientemin=False
dic={'38599.5':[[18976567,1,100,38601,38597]]}
datis=[38000,38005,38004,38600,38590]
minutos=0

while True:
    #bars = exchange.fetch_ohlcv('XBTUSD', timeframe='1m', limit=61)
    #df = pd.DataFrame(bars[:-1], columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    #datos = df.close.tolist()
    minutos=minutos+1
    ultimo=datis.pop()
    maximo=datis[0]
    minimo=datis[3]
    #ultimo=datos.pop()
    #if ultimo>maximo:
     #   maximo=ultimo
     #   smax=True
    #if ultimo<minimo:
     #   minimo=ultimo
      #  smin=True




    veinte=(maximo-minimo)*0.80+minimo
    treinta = (maximo - minimo) * 0.70 + minimo
    cuarenta = (maximo - minimo) * 0.60 + minimo
    cinquenta = (maximo + minimo) // 2
    sesenta=(maximo-minimo)*0.40+minimo
    setenta = (maximo - minimo) * 0.30 + minimo
    ochenta=(maximo - minimo) * 0.20 + minimo
    distancia=maximo-minimo
    #fechas = df.time.tolist()
    #fecha = fechas.pop()
    #fechita=datetime.datetime.fromtimestamp(fecha / 1000)
    #print("Maximo:", maximo, "Minimo:", minimo, "Cinquenta:", cinquenta, "Treinta:", treinta,"Setenta:",setenta, "Ultimo:", ultimo, "Distancia:",distancia,"Fecha:",fechita)

    #ORDENES

   #print(exchange.fetch_open_orders())

    # exchange.createOrder('XBTUSD', 'market', 'sell', 200, ...)

    def añadir_precio():
        pass


    def ejecutar_orden(lista):
        if lista[1]==0:
            pass
        if lista[1] == 1:
            pass
        if lista[1] == 2:
            exchange.cancelOrder()
            pass
        if lista[1] == 3:
            exchange.cancelOrder()
            pass

    #LOGICA DE COMPRA

    if abs(distancia)>500:


        #después de máximo

        if siguientemax and( ultimo<maximo or ultimo>treinta) :

            first = exchange.createOrder('XBTUSD', 'limit', 'buy', 100,treinta)
            id = str(first)[22:58]


            tkp = exchange.createOrder('XBTUSD', 'limit', 'sell', 100, treinta)
            id2=str(tkp)[22:58]

            sl = exchange.createOrder('XBTUSD', 'market', 'sell', 100)
            id3=str(sl)[22:58]


            #Metemos take profit en el diccionario

            if dic[str(veinte)]!=None:
                dic[str(veinte)]=[[id2, 2,100, id3]]
            else:
                dic[str(veinte)].append([id2, 2,100, id3])

            #Metemos stop loss en el diccionario

            if dic[str(minimo)]!=None:
                dic[str(minimo)]=[[id3, 4,100, id2]]
            else:
                dic[str(minimo)].append([[id3, 4, 100, id2]])

        #después de mínimo

        if siguientemin and( ultimo>minimo or ultimo<setenta):

            first = exchange.createOrder('XBTUSD', 'limit', 'sell', 100,setenta)
            id = str(first)[22:58]
            #dic[str(treinta)] = [[id, 1,cantidad, treinta, veinte, minimo]]

            #Take profit

            if dic[str(ochenta)]!=None:
                dic[str(ochenta)] = [[id, 3, 100, treinta, veinte, minimo]]
            else:
                dic[str(ochenta)].append([id, 3, 100, treinta, veinte, minimo])

            #Stop loss

            if dic[str(minimo)]!=None:
                dic[str(minimo)] = [[id, 5, 100, treinta, veinte, minimo]]
            else:
                dic[str(minimo)].append([id, 2, 100, treinta, veinte, minimo])


        #situación normal
        penultimo=datis.pop()
        distancia=ultimo-penultimo
        buscar=[ultimo]

        while abs(distancia)>0:
            if ultimo>penultimo:
                penultimo=penultimo+0.5
                buscar.append[penultimo]
                distancia=abs(distancia)-0.5

            if ultimo<penultimo:
                ultimo = ultimo + 0.5
                buscar.append(ultimo)
                distancia = abs(distancia) - 0.5
        print(buscar)
        for precio in buscar:
            if str(precio) in dic:
                for orden in dic[str(precio)]:
                    print(orden)
                    #ejecutar_orden(orden)





    siguientemax = False
    siguientemin = False





    '''
    if smax:
        siguientemax=True
    if smin:
        siguientemin=True


    smin=False
    smax=False
    '''

    if minutos==60:
        minutos=0
        maximo=99999999
        minimo=0




#Plottear retrocesos
    '''
    df = pd.DataFrame(bars[:-1], columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    y0=0*df.time+minimo
    y1=0*df.time+treinta
    y2=0*df.time+cinquenta
    y3=0*df.time+setenta
    y4=0*df.time+maximo
    plt.plot(df.time, df.close,'b')
    plt.plot(df.time,y0, 'r')
    plt.plot(df.time,y1, 'g')
    plt.plot(df.time, y2, 'm')
    plt.plot(df.time, y3, 'k')
    plt.plot(df.time, y4, 'c')
    
# Guardar imagen

    etiqueta = datetime.datetime.fromtimestamp(fecha / 1000)
    etiqueta=str(etiqueta).replace(":"," ")
    etiqueta= etiqueta=str(etiqueta).replace("-"," ")
    plt.title("Fibonacci")

    plt.savefig(str(etiqueta))
    plt.clf()





# Mostrar el mercado a partir de dataframe con velas
    
    for m in bars:
        fecha = datetime.datetime.fromtimestamp(m[0] / 1000)
        m[0] = fecha

    df = pd.DataFrame(bars[:-1], columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    df.index = pd.DatetimeIndex(df['time'])

    mpf.plot(
        df,
        type='candle',
        style='charles',
        title='BTCUSD, 02 March - 2022',
        ylabel='Price ($)',
        volume=True,
        ylabel_lower='Shares\nTraded',
    )
    '''
    time.sleep(60)
