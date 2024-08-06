
import random
from itertools import product

class Estrategia:
    def __init__(self, memoria):
        self.memoria = memoria
        self.puntajeVirtual = 0
        self.estrategia = None

    def darEstrategiaAleatoria(self)->dict:
        if self.estrategia != None:
            self.estrategia = None
        tupla = (0, 1)
        llaves_diccionario = [''.join(map(str, tup)) for tup in list(product(tupla, repeat = self.memoria))]
        aleatorios = list(random.choices(tupla, k = 2**self.memoria))
        result_dict = dict(zip(llaves_diccionario, aleatorios))
        self.estrategia = result_dict
    
    
    def __str__(self):
        print(self.estrategia)

    def darDiccionario(self):
        return(self.estrategia)

    def isEqual(self,diccionarioAComparar):
        return(self.estrategia == diccionarioAComparar)
    
    def darDecision(self, historiaMercado):
        return(self.estrategia[historiaMercado])
    
    def actualizarPuntajeVirtual(self, historiaMercado, minoria, cambioPuntaje):
        if self.estrategia[historiaMercado] == minoria:
            self.puntajeVirtual += cambioPuntaje
        else:
            self.puntajeVirtual -= cambioPuntaje

    def darPuntajeVirtual(self):
        return(self.puntajeVirtual)



