from AgenteClass import Agente
import random
from itertools import product
import numpy as np

class Mercado:

    def __init__(self,agentes,memoria,cantidadEstrategias) -> None:
        tupla = (0, 1)
        self.historiaMercado = random.choice([''.join(map(str, tup)) for tup in list(product(tupla, repeat = memoria))])
        self.agentes = []      
        for i in range(agentes):
            agente = Agente(memoria,cantidadEstrategias)
            self.agentes.append(agente)
        self.precio = 100
        self.historiaPrecio = [self.precio]
        self.registroMinoria = [int(self.historiaMercado[-1])]
        self.registroDecisiones = [np.nan]

    @staticmethod
    def calcularMinoria(arreglo_decisiones):
        minoria = 1-round(np.sum(arreglo_decisiones)/len(arreglo_decisiones))
        return(minoria)

    @staticmethod
    def cambioPuntaje():
        #Este cambio en el puntaje se puede modelar proporcional al cambio en la minoria
        return(1)
    

    def actualizarPrecio(self, arreglo_decisiones):
        A_t = sum(arreglo_decisiones) - (len(arreglo_decisiones) - sum(arreglo_decisiones))
        
        self.precio *= np.exp(A_t / len(arreglo_decisiones))
        
        self.historiaPrecio.append(self.precio)
        
        self.registroDecisiones.append(sum(arreglo_decisiones))
    

    def actualizarHistoria(self, minoria):
        self.historiaMercado = self.historiaMercado.replace(self.historiaMercado[0],"",1)
        self.historiaMercado = self.historiaMercado + str(minoria)
        self.registroMinoria.append(int(minoria))


    def correrRonda(self):
        
        arreglo_decisiones = np.repeat([-1],len(self.agentes))

        for i in range(len(self.agentes)):
            arreglo_decisiones[i] = self.agentes[i].tomarDecision(self.historiaMercado)
        
        minoria = self.calcularMinoria(arreglo_decisiones)
        cambioPuntaje = self.cambioPuntaje()

        for agnt in self.agentes:
            agnt.actualizarPuntaje(self.historiaMercado, minoria, cambioPuntaje)

        self.actualizarHistoria(minoria)
        self.actualizarPrecio(arreglo_decisiones)

    


    def __str__(self) -> str:
        print('Historia: ',self.historiaMercado, '\n')
        i = 0
        for agnt in self.agentes:
            i += 1
            print('Agente ',i,':')
            print('Puntaje Real: ', agnt.darPuntajeReal())
            print(agnt.__str__(),'\n')
            print("------------------------------------------------")