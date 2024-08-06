from ExperimentoClass import Experimento
import numpy as np
import pandas as pd
from torchmetrics.regression import KLDivergence
from torch import tensor
from bayes_opt import BayesianOptimization

class Opti:

    def __init__(self, model, numRondas = 100, numExperimentos = 10) -> None:
        self.model = model
        self.numRondas = numRondas
        self.numExperimentos = numExperimentos

    def get_sim_data(self, agents, memory, strats):

        experimento = Experimento(numeroRondas = self.numRondas,
                                    cantidadAgentes = agents,
                                    memoria = memory,
                                    cantidadEstrategias = strats,
                                    modelo = self.model)
        df = experimento.ejecutarExperimento()
        sim_data = np.log(df.Precio).diff().tolist()[1:]

        return sim_data
    
    def get_price_data(self, agents, memory, strats):
        experimento = Experimento(numeroRondas = self.numRondas,
                                cantidadAgentes = agents,
                                memoria = memory,
                                cantidadEstrategias = strats,
                                modelo = self.model)
        df = experimento.ejecutarExperimento()
        df = df.rename(columns = {'Precio': 'Close'})
        return df

    def prob_emp(self, lista_de_numeros, nbins = 50, minim =- 1, maxim = 1):
        lista_de_numeros = lista_de_numeros
        lista_de_numeros.sort()

        #intervalos = np.linspace(minim, maxim, nbins)
        intervalos = np.linspace(min(lista_de_numeros), max(lista_de_numeros), nbins)
        frecuencia_relativa = []
        tamaño_lista = len(lista_de_numeros)
        percentil_prev = - np.inf

        for valor_percentil in intervalos:
            cuenta = len([x for x in lista_de_numeros if percentil_prev < x <= valor_percentil])
            frecuencia_relativa.append(cuenta / tamaño_lista)
            percentil_prev = valor_percentil

        return frecuencia_relativa

    def audit_freq_(self, p, q):
        len_p = len(p)
        len_q = len(q)

        #max_iter = 200
        #contador = 0
        while (0 in q) or (0 in p):  # Continuar mientras haya ceros en p o en q
            #contador += 1
            #assert contador <= max_iter

            # Sumar hacia la izquierda los valores diferentes de cero en la lista p cuando q tiene ceros
            for i in range(1, len(q)):
                if q[i] == 0:
                    p[i - 1] += p[i]
                    p[i] = 0

            # Sumar hacia la izquierda los valores diferentes de cero en la lista q cuando p tiene ceros
            for i in range(1, len(p)):
                if p[i] == 0:
                    q[i - 1] += q[i]
                    q[i] = 0

            # Eliminar los ceros en ambas listas
            p = [valor for valor in p if valor != 0]
            q = [valor for valor in q if valor != 0]

            # Ajustar la longitud de ambas listas para que tengan la misma longitud
            len_p = len(p)
            len_q = len(q)

            if len_p < len_q:
                p += [0] * (len_q - len_p)
            elif len_q < len_p:
                q += [0] * (len_p - len_q)
            #print (p, q)

        return p, q
    

    def audit_freq(self, p, q):
        a = []
        b = []

        juntando = False
        
        for i in range(len(p)):
            if not juntando and (p[i] == 0 or q[i] == 0):
                temp_a = 0
                temp_b = 0
                juntando = True
            elif not juntando:
                a.append(p[i])
                b.append(q[i])
            
            if juntando:
                temp_a += p[i]
                temp_b += q[i]
                if temp_a * temp_b != 0:
                    juntando = False
                    a.append(temp_a)
                    b.append(temp_b)

        return a, b

    def get_kl(self, agents, memory, strats):

        results = []

        for i in range(self.numExperimentos):
            sim_data = self.get_sim_data(agents, memory, strats)

            if any(np.isnan(x) for x in sim_data) or any(np.isinf(x) for x in sim_data):
                results.append(100)
            else:
                sim_freqs = self.prob_emp(sim_data)
                datos = self.datos
                real_freqs = self.prob_emp(datos)
                
                p, q = self.audit_freq(real_freqs, sim_freqs)
                p = tensor([p])
                q = tensor([q])
                
                kl_divergence = KLDivergence()
                results.append(kl_divergence(p, q).item())

        return sum(results) / len(results)


    def cargar_datos(self, archivo, is_logs = False):
        try:
            self.datos = pd.read_csv(archivo)
        except:
            self.datos = archivo

        

        self.datos = self.datos['Close']

        if not is_logs:
            self.datos = np.log(self.datos).diff().tolist()[1:]
            self.datos = [x for x in self.datos if not (np.isinf(x) or np.isnan(x))]
        
        self.datos = list(self.datos)
        


    def encontrar_minimo(self, params, init_points, n_iter):

        optimizer = BayesianOptimization(
            #f = Opti().get_kl,
            f = self.func_opt,
            pbounds = params,
            verbose = 0, # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
            random_state = 1
        )

        optimizer.maximize(
            init_points = init_points, #Random explor 
            n_iter = n_iter
        )

        if self.model != 'BM':
            minimo = optimizer.max['target']
            n_agentes = int(optimizer.max['params']['agents']) if int(optimizer.max['params']['agents']) % 2 != 0 else int(optimizer.max['params']['agents']) + 1
            parametros_minimos = [n_agentes, int(optimizer.max['params']['memory']), int(optimizer.max['params']['strats'])]
        else:
            minimo = optimizer.max['target']
            parametros_minimos = [optimizer.max['params']['agents'], optimizer.max['params']['memory'], optimizer.max['params']['strats']]

        return -minimo, parametros_minimos
    

    def func(self, agents, memory, strats):
        return -self.get_kl(agents, memory, strats)
    
    def func_opt(self, agents, memory, strats):
        if self.model != 'BM':
            agents = int(agents)
            memory = int(memory)
            strats = int(strats)
            if agents % 2 == 0:
                agents += 1
        return self.func(agents, memory, strats)



