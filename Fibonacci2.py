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


#RESETEA EL FIBONACCI
maximo=0
minimo=99999

#Nos dice si estamos en la siguiente vela de un máximo
siguientemax=False
siguientemin=False

#DICCIONARIO
#dic={'1':[1897,1456,1005,3861,3858,0] , '2':[2354,1534,1008,3860,3978,1]}
'''datis=[38000,38005,38004,38600,38580]'''
dic={}
#CONTADORES
minutos=0
segundos=0

#si esta vacio el diccionario
vaciodic=True

#Se utilizan para saber si es máximo el dato actual
soymin=False
soymax=False

#Se usa para saber si ya hemos actualizado el take profit
harotoid2=False
harotoid3=False

#es el contador para añadir claves al diccionario
clavedic=1

#Guarda las ids de las ordenes abiertas
abiertas=[]

#Se usa para borrar ordenes del diccionario
paraborrar=[]

#Se usa para poner el primer take profit
tocado30=False

while True:

    while segundos == 60 or vaciodic:
        time.sleep(60)
        bars = exchange.fetch_ohlcv('XBTUSD', timeframe='1m', limit=61)
        df = pd.DataFrame(bars[:-1], columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        datos = df.close.tolist()
        minutos=minutos+1
        #ultimo=datis.pop()
        #maximo=datis[0]
        #minimo=datis[3]
        ultimo=datos.pop()
        if ultimo>maximo:
            maximo=ultimo
            soymax=True
        if ultimo<minimo:
            minimo=ultimo
            soymin=True

        veinte=(maximo-minimo)*0.80+minimo
        treinta = (maximo - minimo) * 0.70 + minimo
        cuarenta = (maximo - minimo) * 0.60 + minimo
        cinquenta = (maximo + minimo) // 2
        sesenta=(maximo-minimo)*0.40+minimo
        setenta = (maximo - minimo) * 0.30 + minimo
        ochenta=(maximo - minimo) * 0.20 + minimo
        distancia=maximo-minimo

        print("Maximo:", maximo, "Minimo:", minimo, "Cinquenta:", cinquenta, "Treinta:", treinta,"Setenta:",setenta, "Ultimo:", ultimo, "Distancia:",distancia)
        if abs(distancia)>5:

            #después de máximo

            if siguientemax and ultimo<=maximo and ultimo>treinta :
                orden1 = exchange.createOrder('XBTUSD', 'limit', 'buy', 100, treinta)
                id1 = str(orden1)[22:58]
                orden2 = exchange.createOrder('XBTUSD', 'limit', 'buy', 100, cinquenta)
                id2 = str(orden2)[22:58]
                orden3 = exchange.createOrder('XBTUSD', 'limit', 'buy', 100, setenta)
                id3 = str(orden3)[22:58]

                id4=None

                params = {
                    'stopPx': minimo,  # if needed
                }

                sl = exchange.create_order('XBTUSD', 'Stop', 'sell', 300, None, params)
                id5 = str(sl)[22:58]
                dic[str(clavedic)]=[id1,id2,id3,id4,id5,0]
                vaciodic=False
                clavedic+=1


                print("Lanzamos grupo de ordenes desde máximo")

            #después de mínimo

            if siguientemin and ultimo>=minimo and ultimo<setenta:
                orden1 = exchange.createOrder('XBTUSD', 'limit', 'sell', 100, setenta)
                id1 = str(orden1)[22:58]
                orden2 = exchange.createOrder('XBTUSD', 'limit', 'sell', 100, cinquenta)
                id2 = str(orden2)[22:58]
                orden3 = exchange.createOrder('XBTUSD', 'limit', 'sell', 100, treinta)
                id3 = str(orden3)[22:58]


                id4=None
                params = {
                    'stopPx': maximo,  # if needed
                }

                sl = exchange.create_order('XBTUSD', 'Stop', 'buy', 300, None, params)
                id5 = str(sl)[22:58]
                dic[str(clavedic)]=[id1,id2,id3,id4,id5,1]
                vaciodic=False
                clavedic += 1
                print("Lanzamos grupo de ordenes desde mínimo")



        #situación normal

        siguientemax = False
        siguientemin = False


        if soymax:
            siguientemax=True
        if soymin:
            siguientemin=True


        soymin=False
        soymax=False


        if minutos==60:
            minutos=0
            maximo=99999999
            minimo=0
        segundos=0


#CADA DOS SEGUNDOS COMPRUEBA SI HAY ACTUALIZACIÓN
#poner abiertas antes o despues

    for grupo in dic:


        opened = exchange.fetch_open_orders()

        for dicts in opened:
            idcancel = dicts['id']
            if idcancel not in abiertas:
                abiertas.append(idcancel)

        print("Estamos en el grupo de ordenes numero:",grupo)
        #print(abiertas)
        #print("id tk:",dic[str(grupo)][3])



        if  dic[str(grupo)][3] != None and dic[str(grupo)][3] not in abiertas :
                # TAKE PROFIT SIMPLE
                #CANCEL ID2
                exchange.cancel_order(dic[str(grupo)][1])
                # CANCEL id3
                exchange.cancel_order(dic[str(grupo)][2])
                # CANCEL STOP LOSS
                exchange.cancel_order(dic[str(grupo)][4] )
                #BORRAR DEL DICCIONARIO
                if (str(grupo) in dic):
                    paraborrar.append(str(grupo))

        elif dic[str(grupo)][0] not in abiertas :

                if dic[str(grupo)][3]==None:
                    #ESTABLECER TAKE PROFIT
                    if dic[str(grupo)][5] == 0:
                        tk=exchange.createOrder('XBTUSD', 'limit', 'sell', 100, veinte)
                        id4 = str(tk)[22:58]
                    elif dic[str(grupo)][5] == 1:
                        tk=exchange.createOrder('XBTUSD', 'limit', 'buy', 100, ochenta)
                        id4 = str(tk)[22:58]

                    dic[str(grupo)][3]=id4




                elif dic[str(grupo)][1]  not in abiertas   and harotoid2==False:
                    harotoid2=True
                    #recolocar TAKE PROFIT1 a 40 o a 60

                    exchange.cancel_order(str(dic[str(grupo)][3]))

                    if dic[str(grupo)][5]==0:
                        tk=exchange.createOrder('XBTUSD', 'limit', 'sell', 200, cuarenta)
                        id4 = str(tk)[22:58]
                        dic[str(grupo)][3]=id4
                    elif dic[str(grupo)][5]==1:
                        tk=exchange.createOrder('XBTUSD', 'limit', 'buy', 200, sesenta)
                        id4 = str(tk)[22:58]
                        dic[str(grupo)][3]=id4



                elif dic[str(grupo)][1]   not in abiertas and dic[str(grupo)][2]  not in abiertas and harotoid3==False  :

                    harotoid3=True
                    # recolocar TAKE PROFIT2 A 60 o a 40

                    exchange.cancel_order(str(dic[str(grupo)][3]))
                    if dic[str(grupo)][5] == 0:
                        tk=exchange.createOrder('XBTUSD', 'limit', 'sell', 300, sesenta)
                    elif dic[str(grupo)][5] == 1:
                        tk=exchange.createOrder('XBTUSD', 'limit', 'buy', 300, cuarenta)



                elif sl not in abiertas:
                    # BORRAR DEL DICCIONARIO
                    if (str(grupo) in dic):
                        paraborrar.append(str(grupo))

    for borrar in paraborrar:
        if str(borrar) in dic:
            del dic[str(borrar)]

    segundos+=2
    print("Checkeando...")
    print("Diccionario:",dic)
    time.sleep(2)
