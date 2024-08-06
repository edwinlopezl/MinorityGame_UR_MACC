from MercadoClass_MG import Mercado as mercadoMG
from MercadoClass_DG import Mercado as mercadoDG
from MercadoClass_BM import Mercado as mercadoBM
import numpy as np
import pandas as pd



class Experimento:

    def __init__(self, numeroRondas, cantidadAgentes, memoria, cantidadEstrategias, modelo) -> None:

        if modelo == 'MG_DO':
            self.mercado = mercadoMG(cantidadAgentes, memoria, cantidadEstrategias)
            self.historiaPuntaje = np.zeros((numeroRondas, cantidadAgentes))
            self.numeroRondas = numeroRondas
            self.cantidadAgentes = cantidadAgentes
            self.memoria = memoria
            self.cantidadEstrategias = cantidadEstrategias

        elif modelo == 'MG_Lambda':
            self.mercado = mercadoDG(cantidadAgentes, memoria, cantidadEstrategias)
            self.historiaPuntaje = np.zeros((numeroRondas, cantidadAgentes))
            self.numeroRondas = numeroRondas
            self.cantidadAgentes = cantidadAgentes
            self.memoria = memoria
            self.cantidadEstrategias = cantidadEstrategias

        elif modelo == 'BM':
            self.mercado = mercadoBM(cantidadAgentes, memoria, cantidadEstrategias)
            #Este array lleva registro de historia de puntajes
            self.numeroRondas = numeroRondas
            self.cantidadAgentes = cantidadAgentes
            self.memoria = memoria
            self.cantidadEstrategias = cantidadEstrategias

        else:
            print("Modelo incorrecto, las opciones son ['MG_DO', 'MG_Lambda', 'BM']")

    
    def ejecutarExperimento(self):
        for i in range(self.numeroRondas):
            self.mercado.correrRonda()
            #for j in range(self.cantidadAgentes):
            #    self.historiaPuntaje[i,j] = self.mercado.agentes[j].darPuntajeReal()
        return(self.to_pandas())

    
    def __str__(self) -> str:
        print(self.mercado.precio)
        #print(self.historiaPuntaje)


    def to_pandas(self) -> pd.DataFrame:
        return(pd.DataFrame({'Precio': self.mercado.historiaPrecio,
                             #'Minoria': self.mercado.registroMinoria,
                             #'Num_A': self.mercado.registroDecisiones,
                             'Ronda': list(range(self.numeroRondas + 1))}))
