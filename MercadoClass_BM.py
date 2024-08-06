from AgenteClass import Agente
import random
from itertools import product
import numpy as np


class Mercado:

    def __init__(self,agentes,memoria,cantidadEstrategias) -> None:
        self.Mu = agentes
        self.Sigma = memoria
        self.precio = 100
        self.cantidadEstrategias = cantidadEstrategias
        self.historiaPrecio = [self.precio]
        self.registroMinoria = [np.nan]
        self.registroDecisiones = [np.nan]




    def actualizarPrecio(self, pMu, pSigma):
        cambioNormal = random.normalvariate(mu = pMu, sigma = pSigma/np.sqrt(252))
        self.precio *= np.exp(cambioNormal)
        self.historiaPrecio.append(self.precio)
        self.registroMinoria.append(np.nan)
        self.registroDecisiones.append(np.nan)
        
    


    def correrRonda(self):
        self.actualizarPrecio(pMu = self.Mu, pSigma=self.Sigma)

    


    def __str__(self) -> str:
        print(self.historiaPrecio)