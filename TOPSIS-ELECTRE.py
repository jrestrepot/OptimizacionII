# -*- coding: utf-8 -*-
"""Parcial2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EMJbnFZugBO-P5hdLLkpaksmkXIBvKtx

##IMPLEMENTACIÓN TOPSIS
"""

def normaLP(matrizV, lp: str or int):
  '''
  Método auxiliar. Halla la norma de cada columna en una matriz.
  '''
  normas = []
  if lp == "infinity":
    matrizT = list(map(list, zip(*matrizV)))
    for i in range(len(matrizT)):
      normas.append(max(matrizT[i]))
  else:
    for j in range(len(matrizV[0])):
      suma = 0
      for i in range(len(matrizV)):
        suma = suma + abs(matrizV[i][j]**lp)
      normaJ = (suma)**(1./lp)
      normas.append(normaJ)
  return(normas)

def normalizarPond(matrizV, lp: str or int, pesos):
  '''
  Método auxiliar. Normaliza y pondera la matriz de decisión.
  '''
  normas = normaLP(matrizV, lp)
  for i in range(len(matrizV)):
    for j in range(len(matrizV[i])):
      matrizV[i][j] = matrizV[i][j]/normas[j]*pesos[j]
  return matrizV

def TOPSIS(matrizV, lp: str or int, pesos, tipo): 

  '''
  Implementación del método TOPSIS.
  Imprime el ranking de las alternativas, con sus respectivas proximidades a la solución ideal.

  Parámetros: 
  matrizV: Matriz de decisión, una lista de listas.
  lp: Norma que el usuario desee utilizar. Ej: 1, 2, "infinity".
  pesos: Lista de pesos en el mismo orden en el que van sus criterios correspondientes.
  tipo: Una lista de strs en donde se determina si el criterio es deseable o indeseable.
        Ej: ["deseable", "indeseable", "indeseable"]
  '''

  matrizPond = normalizarPond(matrizV, lp, pesos)
  ideales = []
  antiIdeales = []
  proximidad = []
  matrizT = list(map(list, zip(*matrizPond))) #Matriz traspuesta

  for i in range(len(matrizT)):
    if tipo[i] == "deseable":
      ideales.append(max(matrizT[i]))
      antiIdeales.append(min(matrizT[i]))
    else:
      ideales.append(min(matrizT[i]))
      antiIdeales.append(max(matrizT[i]))

  distAntiIdeal = []
  distIdeal = []

  if lp == "infinity":
    for i in range(len(matrizPond)):
      resta1 = []
      resta2 = []
      for j in range(len(matrizPond[i])):
        resta1.append(abs((ideales[j] - matrizPond[i][j])))
        resta2.append(abs((antiIdeales[j] - matrizPond[i][j])))
      distIdeal.append(max(resta1))
      distAntiIdeal.append(max(resta2))
      proximidad.append(distAntiIdeal[i]/(distIdeal[i]+distAntiIdeal[i]))
  else:
    for i in range(len(matrizPond)):
      suma1 = 0
      suma2 = 0
      for j in range(len(matrizPond[i])):
        suma1 = suma1 + abs((ideales[j] - matrizPond[i][j])**lp)
        suma2 = suma2 + abs((antiIdeales[j] - matrizPond[i][j])**lp)
      distIdeal.append((suma1)**(1./lp))
      distAntiIdeal.append((suma2)**(1./lp))
      proximidad.append(distAntiIdeal[i]/(distIdeal[i]+distAntiIdeal[i]))
  
  for i in range(len(proximidad)):
    proximidad[i] = (proximidad[i], "alternativa " + str(i+1))
  proximidad.sort(reverse=True)

  print("El ranking de las soluciones es el siguiente:")

  for i in range(len(proximidad)):
    print("La alternativa en el puesto número " + str(i+1) + " es la " + str(proximidad[i][1]) + " con una proximidad a la solución ideal de " + str(proximidad[i][0]))

#TOPSIS([[185,6.5,12.85],[290,7.5,13.695],[310,7.6,12.87],[245, 6.5,11.385],[325,7.55, 11.235],[235,6.85, 12.525]], 2,[0.3,0.4,0.3], ["indeseable", "indeseable", "deseable"])
TOPSIS([[1,5],[4,2],[3,3]], 1, [0.5,0.5], ["deseable", "deseable"])

"""##IMPLEMENTACIÓN ELECTRE

"""

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def normalizar(matrizV, pesos, tipo):
  '''
  Método auxiliar. Normaliza usando la distancia relativa.
  '''
  matrizT = list(map(list, zip(*matrizV)))
  matrizNorm = matrizV
 
  for i in range(len(matrizV)):
    for j in range(len(matrizV[i])):
      if tipo[j] == "deseable":
        matrizNorm[i][j] = ((matrizNorm[i][j] - min(matrizT[j]))/(max(matrizT[j])-min(matrizT[j])))
      else:
        matrizNorm[i][j] = ((max(matrizT[j])- matrizNorm[i][j])/(max(matrizT[j])-min(matrizT[j])))
  
  return matrizNorm
  
normalizar([[1,5],[4,2],[3,3]], [0.5,0.5], ["deseable", "deseable"])

def ponderar(matrizV,pesos,tipo):
  '''
  Método auxiliar. Pondera la matriz normalizada.
  '''
  matrizT = list(map(list, zip(*matrizV)))
  matrizPond = matrizV
 
  for i in range(len(matrizV)):
    for j in range(len(matrizV[i])):
      if tipo[j] == "deseable":
        matrizPond[i][j] = ((matrizPond[i][j] - min(matrizT[j]))/(max(matrizT[j])-min(matrizT[j])))*pesos[j]
      else:
        matrizPond[i][j] = ((max(matrizT[j])- matrizPond[i][j])/(max(matrizT[j])-min(matrizT[j])))*pesos[j]
  
  return matrizPond
ponderar([[1,5],[4,2],[3,3]], [0.5,0.5], ["deseable", "deseable"])

def concordancia(matrizNorm, pesos):
  '''
  Devuelve la matriz de concordancia.
  Parámetros: 
  matrizNorm: Matriz normalizada.
  pesos: Lista de pesos.
  '''
  matrizConcor = np.zeros((len(matrizNorm), len(matrizNorm)))

  for i in range(len(matrizNorm)):
    for j in range(len(matrizNorm)):
      for k in range(len(matrizNorm[i])):
        if i==j:
          matrizConcor[i][j]=np.nan
        else:
          if matrizNorm[i][k]==matrizNorm[j][k]:
            matrizConcor[i][j] = matrizConcor[i][j]+pesos[k]*0.5
          if matrizNorm[i][k]>matrizNorm[j][k]:
            matrizConcor[i][j] = matrizConcor[i][j]+pesos[k]
          else:
            continue
  return matrizConcor

def dominanciaConcordante(matrizConcor, c):
  '''
  Devuelve la matriz de dominancia concordante a partir de la matriz de concordancia.
  Parámetros: 
  matrizConcor: matriz concordante.
  c: valor límite para el índice de concordancia.
  '''
  matrizDominC= np.zeros((len(matrizConcor), len(matrizConcor)))

  for i in range(len(matrizConcor)):
    for j in range(len(matrizConcor[i])):
      if i==j:
        matrizDominC[i][j] = np.nan
      else:
        if matrizConcor[i][j]>c:
          matrizDominC[i][j] = 1
        else:
          matrizDominC[i][j] = 0

  return matrizDominC

def discordancia(matrizV, pesos, tipo):
  '''
  Devuelve la matriz de discordancia.
  Parámetros: 
  matrizV: Matriz de decisión.
  pesos: Lista de pesos.
  tipo: Lista de strs que definen si el criterio es deseable o indeseable.
  '''
  matrizPond = ponderar(matrizV,pesos,tipo)
  matrizDiscor = np.zeros((len(matrizPond), len(matrizPond)))
  for i in range(len(matrizPond)):
    for j in range(len(matrizPond)):
       diff = []
       diff2 = []
       for k in range(len(matrizPond[i])):
         if matrizPond[j][k]>matrizPond[i][k]:
           diff2.append(matrizPond[j][k]-matrizPond[i][k])
         diff.append(abs(matrizPond[j][k]-matrizPond[i][k]))
       if i==j:
          matrizDiscor[i][j]=np.nan
       else:
        if len(diff2) == 0:
          matrizDiscor[i][j] = 0
        else:
          matrizDiscor[i][j]=(max(diff2))/(max(diff))
  return matrizDiscor

def dominanciaDiscordante(matrizDiscor, d):
  '''
  Devuelve la matriz de dominancia discordante a partir de la matriz de discordancia.
  Parámetros: 
  matrizDiscor: matriz de discordancia.
  d: valor límite para el índice de discordancia.
  '''
  matrizDominD= np.zeros((len(matrizDiscor), len(matrizDiscor)))

  for i in range(len(matrizDiscor)):
    for j in range(len(matrizDiscor[i])):
      if i==j:
        matrizDominD[i][j] = np.nan
      else:
        if matrizDiscor[i][j]<d:
          matrizDominD[i][j] = 1
        else:
          matrizDominD[i][j] = 0

  return matrizDominD

def ELECTRE(matrizV, pesos, tipo, c, d):
  '''
  Imprime el grafo ELECTRE y devuelve la matriz de dominancia agregada.
  Parámtros:
  matrizV: matriz de decisión. Lista de listas.
  pesos: lista de pesos de cada criterio (en orden).
  tipo: lista de strs que determine si el criterio es deseable o indeseable (en orden)
  c: umbral para la concordancia. Número flotante.
  d: umbral para la discordancia. Número florante.
  '''


  matrizNorm = normalizar(matrizV, pesos, tipo)
  matrizConcor = concordancia(matrizNorm, pesos)
  matrizDominC = dominanciaConcordante(matrizConcor, c)
  matrizPond = ponderar(matrizV,pesos,tipo)
  matrizDiscor = discordancia(matrizPond,pesos,tipo)
  matrizDominD = dominanciaDiscordante(matrizDiscor, d)

  dominanciaAgregada = np.zeros((len(matrizDominD),len(matrizDominD)))
  for i in range(len(matrizDominC)):
    for j in range(len(matrizDominC[i])):
      dominanciaAgregada[i][j] = matrizDominC[i][j]*matrizDominD[i][j]
  

  nombreCol = []
  for i in range(len(dominanciaAgregada)):
    nombreCol.append('Alternativa ' + str(i+1))

  dominanciaAgregada1 = pd.DataFrame(dominanciaAgregada, columns = nombreCol, index = nombreCol)
  '''
  Imprimir el grafo
  '''

  Grafo = nx.Graph()
  for i in range(len(dominanciaAgregada)):
    Grafo.add_node("A" + str(i+1))

  for i in range(len(dominanciaAgregada)):
    for j in range(len(dominanciaAgregada[i])):
      if dominanciaAgregada[i][j] ==1:
          Grafo.add_edge("A" + str(i+1),"A" + str(j+1))

  pos = nx.spring_layout(Grafo)
  nx.draw_networkx_labels(Grafo, pos)
  nx.draw_networkx_nodes(Grafo, pos, node_color='c')
  nx.draw_networkx_edges(Grafo, pos, edge_color='b', arrows=True)
  plt.show()


  return dominanciaAgregada1

  
ELECTRE([[1,5],[4,2],[3,3]], [0.5,0.5], ["deseable", "deseable"], 0.5, 1)
#ELECTRE([[185,6.5,12.85],[290,7.5,13.695],[310,7.6,12.87],[245, 6.5,11.385],[325,7.55, 11.235],[235,6.85, 12.525]], [0.3,0.4,0.3], ["indeseable", "indeseable", "deseable"], 0.5, 0.5)