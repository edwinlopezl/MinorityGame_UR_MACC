from EstrategiaClass import Estrategia
import copy

class Agente:

    def __init__(self, memoria, cantidadEstrategias):

        self.estrategias = []

        for i in range(cantidadEstrategias):

            estrategia = Estrategia(memoria)
            #Si hay ya una estrategia se comprueba que no es repetida
            if i > 0:
                repetida = True
                while repetida:
                    repetida = False
                    estrategia.darEstrategiaAleatoria()
                    for j in range(i):
                        if estrategia.isEqual(self.estrategias[j].darDiccionario()):
                            repetida = True
            #La primera estrategia se selecciona sin comprobar
            else:
                estrategia.darEstrategiaAleatoria()

            self.estrategias.append(estrategia)

        
        self.puntajeReal = 0
        self.ultimaDecision = None

    def tomarDecision(self, historiaMercado):
        mejorEstrategia = copy.deepcopy(self.estrategias[0])
        for est in self.estrategias:
            if est.darPuntajeVirtual() > mejorEstrategia.darPuntajeVirtual():
                mejorEstrategia = copy.deepcopy(est)
        self.ultimaDecision = mejorEstrategia.darDecision(historiaMercado)
        return(self.ultimaDecision)
    

    def actualizarPuntaje(self, historiaMercado, minoria, cambioPuntaje):
        ### acá existe la posibilidad de modificiarlo dividiendo el acumulado sobre P
        if minoria == self.ultimaDecision:
            self.puntajeReal += cambioPuntaje
        else:
            self.puntajeReal -= cambioPuntaje

        for est in self.estrategias:
            est.actualizarPuntajeVirtual(historiaMercado, minoria, cambioPuntaje)

    
    def darPuntajeReal(self):
        return(self.puntajeReal)


    def __str__(self) -> str:
        i = 0
        for est in self.estrategias:
            i += 1
            print('Estrategia ',i,':', est.darDiccionario(), '\nPuntaje Virtual:',est.darPuntajeVirtual())