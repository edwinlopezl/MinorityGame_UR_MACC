from ExperimentoClass import Experimento
import numpy as np
import random
import pandas as pd



experimento = Experimento(numeroRondas = 50,
                          cantidadAgentes = 100,
                          memoria = 6,
                          cantidadEstrategias = 6)

experimento.ejecutarExperimento()

#print(experimento.historiaPuntaje)
print(experimento.mercado.historiaPrecio)

