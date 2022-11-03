import ast
import json

import ccxt
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
import request
import datetime
import time
import mplfinance as mpf
import datetime
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
#'''datis=[38000,38005,38004,38600,38580]'''
dic={}
#CONTADORES
minutos=0
segundos=0
#Se usa para saber si ya hemos actualizado el take profit:
#Si la casilla take profit es None(roto ID1). hr2,hr3 saber si ha roto ID2 Y ID3

#es el contador para añadir claves al diccionario
clavedic=1

#Guarda las ids de las ordenes abiertas
abiertas=[]

#Se usa para borrar ordenes del diccionario
paraborrar=[]
eliminar=[]

#Si es hora nueva
horanueva=False

#Iniciamos diccionario,max y min a partir de un archivo

nombre = input("Introduce nombre de archivo diccionario: ")
archivo = open(nombre, "r")

lineas=archivo.readlines()
dicc=lineas.pop()
maxmin=lineas.pop()

maximo=int(maxmin[7:14])
minimo=int(maxmin[22:29])
dic=ast.literal_eval(dicc)

print(dic,maximo,minimo)

#Abrimos archivo para escribir

archivo = open("Prueba.txt", "w")
archivo.write("Hora encendido: "+str(datetime.datetime.now())+"\n")
print("Hora encendido: ",datetime.datetime.now())

while True:

    while segundos == 60  or not bool(dic):
        if not bool(dic):
            time.sleep(60)
        if horanueva:
            for grupo in dic:
                dic[str(grupo)][11] = False
        segundos=0
        archivo.write(str(datetime.datetime.now())+"\n")
        print(datetime.datetime.now())

        #Cargamos datos del minuto

        bars = exchange.fetch_ohlcv('XBTUSD', timeframe='1m', limit=61)
        df = pd.DataFrame(bars[:-1], columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        datos = df.close.tolist()
        minutos=minutos+1
        ultimo=datos.pop()

        #Calculamos retrocesos

        veinte=(maximo-minimo)*0.80+minimo
        treinta = (maximo - minimo) * 0.70 + minimo
        cuarenta = (maximo - minimo) * 0.60 + minimo
        cinquenta = (maximo + minimo) // 2
        sesenta=(maximo-minimo)*0.40+minimo
        setenta = (maximo - minimo) * 0.30 + minimo
        ochenta=(maximo - minimo) * 0.20 + minimo
        distancia=maximo-minimo
        opened = exchange.fetch_open_orders()
        abiertas = []
        for dicts in opened:
            idcancel = dicts['id']
            if idcancel not in abiertas:
                abiertas.append(idcancel)
        print(" Ultimo:"+ str(ultimo)+" Maximo:"+ str(maximo)+" Minimo:"+ str(minimo)+ " Cinquenta:"+ str(cinquenta)+ " Treinta:"+ str(treinta)+" Setenta:"+str(setenta)+ " Distancia:"+str(distancia)+"\n"+str(abiertas))
        archivo.write(" Ultimo:"+ str(ultimo)+" Maximo:"+ str(maximo)+" Minimo:"+ str(minimo)+ " Cinquenta:"+ str(cinquenta)+ " Treinta:"+ str(treinta)+" Setenta:"+str(setenta)+ " Distancia:"+str(distancia)+"\n"+str(abiertas)+"\n")
        if siguientemax:
            print("Soy siguiente de maximo:")
            archivo.write("Soy siguiente de maximo:\n")
        if siguientemin:
            print("Soy siguiente de minimo:")
            archivo.write("Soy siguiente de minimo:\n")


        if abs(distancia)>50:

            print("Siguientemax:",siguientemax,"maximo>ultimo:",ultimo<maximo,"ultimo > treinta:",ultimo>treinta)
            print("Siguientemin:", siguientemin, "minimo<ultimo:", minimo<ultimo, "ultimo<setenta:",ultimo< setenta)

            # después de máximo
            if siguientemax and ultimo<maximo and ultimo>treinta :

                archivo.write(str(datetime.datetime.now())+"\n")
                print(datetime.datetime.now())
                print("Lanzamos grupo de ordenes desde máximo:\n")
                archivo.write("Lanzamos grupo de ordenes desde máximo:\n")
                orden1 = exchange.createOrder('XBTUSD', 'limit', 'buy', 100, treinta)
                id1 = str(orden1)[22:58]
                print("Orden buy a\n"+str (treinta)+str(id1)+"\n")
                archivo.write("Orden buy a\n"+str (treinta)+"\n"+str(id1)+"\n")
                orden2 = exchange.createOrder('XBTUSD', 'limit', 'buy', 100, cinquenta)
                id2 = str(orden2)[22:58]
                print("Orden buy a\n"+str( cinquenta)+str(id2)+"\n")
                archivo.write("Orden buy a\n" + str(cinquenta)+"\n"+str(id2)+"\n")
                orden3 = exchange.createOrder('XBTUSD', 'limit', 'buy', 100, setenta)
                id3 = str(orden3)[22:58]
                print("Orden buy a\n"+ str( setenta)+str(id3)+"\n")
                archivo.write("Orden buy a\n" + str(setenta)+"\n"+str(id3)+"\n")

                id4=None
                params = {
                    'stopPx': minimo,  # if needed
                    'execInst': 'IndexPrice'
                }

                sl = exchange.create_order('XBTUSD', 'Stop', 'sell', 300, None, params)
                id5 = str(sl)[22:58]
                print("id stop loss:", id5)
                print("Order stop loss sell a:", minimo)
                archivo.write("Order stop loss sell a:"+str( minimo)+"\n")
                tk1 = veinte
                tk2 = cuarenta
                tk3 = sesenta
                hr2 = False
                hr3 = False
                esactual = True
                dic[str(clavedic)]=[id1,id2,id3,id4,id5,0,tk1,tk2,tk3,hr2,hr3,esactual]
                vaciodic=False
                clavedic+=1

            #después de mínimo

            if siguientemin and ultimo>minimo and ultimo<setenta:

                archivo.write(str(datetime.datetime.now())+"\n")
                print(datetime.datetime.now())
                print("Lanzamos grupo de ordenes desde mínimo:\n")
                archivo.write("Lanzamos grupo de ordenes desde mínimo:\n")
                orden1 = exchange.createOrder('XBTUSD', 'limit', 'sell', 100, setenta)
                id1 = str(orden1)[22:58]
                print("Orden sell a\n"+str(setenta)+str(id1)+"\n")
                archivo.write("Orden sell a\n" + str(setenta)+"\n"+str(id1)+"\n")

                orden2 = exchange.createOrder('XBTUSD', 'limit', 'sell', 100, cinquenta)
                id2 = str(orden2)[22:58]
                print("Orden sell a\n"+ str(cinquenta)+str(id2)+"\n")
                archivo.write("Orden sell a\n" + str(cinquenta)+"\n"+str(id2)+"\n")
                orden3 = exchange.createOrder('XBTUSD', 'limit', 'sell', 100, treinta)
                id3 = str(orden3)[22:58]
                print("Orden sell a\n"+str(treinta)+str(id3)+"\n")
                archivo.write("Orden sell a\n" + str(treinta)+"\n"+str(id3)+"\n")


                id4=None
                params = {
                    'stopPx': maximo,  # if needed
                    'execInst': 'IndexPrice'
                }

                sl = exchange.create_order('XBTUSD', 'stop', 'buy', 300, None, params)

                id5 = str(sl)[22:58]
                print("id stop loss:",id5)
                print("Orden stop loss buy a\n"+str(maximo))
                archivo.write("Orden stop loss buy a\n"+str(maximo)+"\n")
                tk1 = ochenta
                tk2 = sesenta
                tk3 = cuarenta
                hr2=False
                hr3=False
                esactual=True
                dic[str(clavedic)]=[id1,id2,id3,id4,id5,1,tk1,tk2,tk3,hr2,hr3,esactual]
                vaciodic=False
                clavedic += 1

        #situación normal
        siguientemax = False
        siguientemin = False
        #if maximo==ultimo:
          #  siguientemax=True

        #if minimo==ultimo:
           # siguientemin=True

        if ultimo >=maximo:
            maximo = ultimo
            siguientemax = True

            for grupo in dic:
                if dic[str(grupo)][11] == True:
                    if dic[str(grupo)][3] == None:
                        print(exchange.cancel_order(dic[str(grupo)][0]))
                        print(exchange.cancel_order(dic[str(grupo)][1]))
                        print(exchange.cancel_order(dic[str(grupo)][2]))
                        print(exchange.cancel_order(dic[str(grupo)][4]))
                        eliminar.append(str(grupo))
                        archivo.write(str(datetime.datetime.now())+"\n")
                        print(datetime.datetime.now())

                        print("Cancelamos ordenes nuevo maximo")
                        archivo.write("Cancelamos ordenes nuevo maximo"+"\n")

            for borrar in eliminar:
                if str(borrar) in dic:
                    del dic[str(borrar)]
            eliminar=[]

        if ultimo <= minimo:
            minimo = ultimo
            siguientemin = True
            for grupo in dic:
                if dic[str(grupo)][11] == True:
                    if dic[str(grupo)][3] == None:
                        print(exchange.cancel_order(dic[str(grupo)][0]))
                        print(exchange.cancel_order(dic[str(grupo)][1]))
                        print(exchange.cancel_order(dic[str(grupo)][2]))
                        print(exchange.cancel_order(dic[str(grupo)][4]))
                    eliminar.append(str(grupo))
                    archivo.write(str(datetime.datetime.now())+"\n")
                    print(datetime.datetime.now())
                    print("Cancelamos ordenes nuevo minimo")
                    archivo.write("Cancelamos ordenes nuevo minimo"+"\n")
            for borrar in eliminar:
                if str(borrar) in dic:
                    del dic[str(borrar)]
            eliminar=[]

        if siguientemax == True:
            print("Viene siguiente de maximo ")
            archivo.write("Viene siguiente de maximo: \n")
        if siguientemin == True:
            print("Viene siguiente de minimo")
            archivo.write("Viene siguiente de minimo: \n")

        horanueva=False
        if minutos==60:
            minutos=0
            maximo=0
            minimo=999999
            horanueva=True
            siguientemax=False
            siguientemin=False

#CADA DOS SEGUNDOS COMPRUEBA SI HAY ACTUALIZACIÓN
#poner abiertas antes o despues??????

    for grupo in dic:

        opened = exchange.fetch_open_orders()
        abiertas=[]
        for dicts in opened:
            idcancel = dicts['id']
            if idcancel not in abiertas:
                abiertas.append(idcancel)

        print("Grupo ordenes:"+str(grupo)+"\n")
        archivo.write("Grupo ordenes:"+str(grupo)+"\n")
        #Comprobamos maximo y minimo de ordenes viejas





        if dic[str(grupo)][11]==False:
            if dic[str(grupo)][5] == 0:
                max = veinte + abs(dic[str(grupo)][7] - dic[str(grupo)][8])
                if ultimo>max:
                    if dic[str(grupo)][3] == None:
                        print(exchange.cancel_order(dic[str(grupo)][0]))
                        print(exchange.cancel_order(dic[str(grupo)][1]))
                        print(exchange.cancel_order(dic[str(grupo)][2]))
                        print(exchange.cancel_order(dic[str(grupo)][4]))
                        if str(grupo) in dic:
                            paraborrar.append(str(grupo))
            else:
                min = ochenta - abs(dic[str(grupo)][7] - dic[str(grupo)][8])
                if ultimo<min:
                    if dic[str(grupo)][3] == None:
                        print(exchange.cancel_order(dic[str(grupo)][0]))
                        print(exchange.cancel_order(dic[str(grupo)][1]))
                        print(exchange.cancel_order(dic[str(grupo)][2]))
                        print(exchange.cancel_order(dic[str(grupo)][4]))
                        if str(grupo) in dic:
                            paraborrar.append(str(grupo))

        #Salida simple take profit
        if  dic[str(grupo)][3] != None and dic[str(grupo)][3] not in abiertas:
                # TAKE PROFIT SIMPLE
                archivo.write(str(datetime.datetime.now())+"\n")
                print(datetime.datetime.now())
                print("Se ha salido por TAKE PROFIT\n")
                archivo.write("Se ha salido por TAKE PROFIT\n")
                print("Cancelamos ID2, ID3 y Stop loss y borramos del dic ...\n")
                archivo.write("Cancelamos ID2, ID3 y Stop loss y borramos del dic ...\n")
                #CANCEL ID2
                if dic[str(grupo)][1] in abiertas:
                    exchange.cancel_order(dic[str(grupo)][1])

                # CANCEL id3
                if dic[str(grupo)][2] in abiertas:
                    exchange.cancel_order(dic[str(grupo)][2])
                # CANCEL STOP LOSS
                exchange.cancel_order(dic[str(grupo)][4])
                #BORRAR DEL DICCIONARIO
                if str(grupo) in dic:
                    paraborrar.append(str(grupo))
        #Si ya ha tocado ID1
        elif dic[str(grupo)][0] not in abiertas :

                if dic[str(grupo)][3]==None:
                    #ESTABLECER TAKE PROFIT
                    archivo.write(str(datetime.datetime.now())+"\n")
                    print(datetime.datetime.now())

                    if dic[str(grupo)][5] == 0:
                        tk=exchange.createOrder('XBTUSD', 'limit', 'sell', 100, dic[str(grupo)][6])
                        id4 = str(tk)[22:58]
                        print("Ponemos take profit en sell\n"+ str(dic[str(grupo)][6]))
                    elif dic[str(grupo)][5] == 1:
                        tk=exchange.createOrder('XBTUSD', 'limit', 'buy', 100, dic[str(grupo)][6])
                        id4 = str(tk)[22:58]
                        print("Ponemos take profit en buy\n"+ str(dic[str(grupo)][6]))
                    dic[str(grupo)][3]=id4

                #e#lif dic[str(grupo)][3]!=None and dic[str(grupo)][9]==False:
                   # pass


                elif dic[str(grupo)][1]  not in abiertas  :
                    if dic[str(grupo)][9]==False:

                        dic[str(grupo)][9]=True
                        #recolocar TAKE PROFIT1 a 40 o a 60
                        archivo.write(str(datetime.datetime.now())+"\n")
                        print(datetime.datetime.now())

                        exchange.cancel_order(str(dic[str(grupo)][3]))
                        if dic[str(grupo)][5]==0:
                            tk=exchange.createOrder('XBTUSD', 'limit', 'sell', 200, dic[str(grupo)][7])
                            id4 = str(tk)[22:58]
                            print("Recolocamos take profit en sell\n"+str( dic[str(grupo)][7]))
                        elif dic[str(grupo)][5]==1:
                            tk=exchange.createOrder('XBTUSD', 'limit', 'buy', 200, dic[str(grupo)][7])
                            id4 = str(tk)[22:58]
                            print("Recolocamos take profit en buy\n"+str( dic[str(grupo)][7]))
                        dic[str(grupo)][3]=id4


                    elif dic[str(grupo)][2]  not in abiertas and dic[str(grupo)][10] ==False  :
                        #ha roto id3
                        dic[str(grupo)][10] = True
                        # recolocar TAKE PROFIT2 A 60 o a 40
                        archivo.write(str(datetime.datetime.now())+"\n")
                        print(datetime.datetime.now())
                        exchange.cancel_order(str(dic[str(grupo)][3]))
                        if dic[str(grupo)][5] == 0:
                            tk=exchange.createOrder('XBTUSD', 'limit', 'sell', 300, dic[str(grupo)][8])
                            id4 = str(tk)[22:58]
                            print("Recolocamos take profit en sell\n", dic[str(grupo)][8])
                            archivo.write("Recolocamos take profit en sell\n" + str(dic[str(grupo)][8])+"\n")
                        elif dic[str(grupo)][5] == 1:
                            tk=exchange.createOrder('XBTUSD', 'limit', 'buy', 300, dic[str(grupo)][8])
                            id4 = str(tk)[22:58]
                            print("Recolocamos take profit en buy\n"+str( dic[str(grupo)][8]))
                            archivo.write("Recolocamos take profit en buy\n"+str( dic[str(grupo)][8])+"\n")
                        dic[str(grupo)][3] = id4

                if dic[str(grupo)][4] not in abiertas:
                    # BORRAR DEL DICCIONARIO
                    #SALIDA POR STOP LOSS
                    if (str(grupo) in dic):
                        paraborrar.append(str(grupo))
                    exchange.cancel_order(dic[str(grupo)][0])
                    exchange.cancel_order(dic[str(grupo)][1])
                    exchange.cancel_order(dic[str(grupo)][2])
                    if dic[str(grupo)][3] != None:
                        exchange.cancel_order(dic[str(grupo)][3])
                    print("Salida por stop loss en "+str(minimo)+"\n")
                    archivo.write("Salida por stop loss en " + str(minimo) + "\n")
    for borrar in paraborrar:
        if str(paraborrar.pop()) in dic:
            del dic[str(borrar)]
    paraborrar=[]
    segundos+=2
    #print("Checkeando...\n")
    print("Diccionario:\n"+str(dic))
    archivo.write("Diccionario:\n"+str(dic)+"\n")
    print(abiertas)
    archivo.write(str(abiertas)+"\n")

    time.sleep(2)
