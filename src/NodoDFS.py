import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoDFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo DFS. '''
        # Tu implementación va aquí
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        # Atributos extra:
        
        self.hijos = []
        self.padre = -1


    def dfs(self, env):
        ''' Algoritmo DFS. '''
        # Tu implementación va aquí
        yield env.timeout(TICK)
        
        if self.id_nodo == 0:
            self.padre = 0
            k = self.nk(self.vecinos)
            self.canal_salida.envia([self.id_nodo,[self.id_nodo],'GO()'],[k])
            self.hijos.append(k)
        
        while True: 
            mensaje = yield self.canal_entrada.get()
            tipo = mensaje[2]
            visitados = mensaje[1]
            pj = mensaje[0]

            if 'GO' in tipo:
                self.padre = pj
                if self.contiene(self.vecinos,visitados):
                    self.canal_salida.envia([self.id_nodo,list(set(visitados) | set([self.id_nodo])),'BACK()'],[pj])
                else:
                    k = self.nk(list(set(self.vecinos) - set(visitados)))
                    self.canal_salida.envia([self.id_nodo,list(set(visitados) | set([self.id_nodo])), 'GO()'],[k])
                    self.hijos.append(k)

            if 'BACK' in tipo:
                if self.contiene(self.vecinos,visitados):
                    if self.padre == self.id_nodo:
                        print("el recorrido termino")
                    else:
                        self.canal_salida.envia([self.id_nodo,visitados,'BACK()'],[self.padre])
                else:
                    k = self.nk(list(set(self.vecinos) - set(visitados)))
                    self.canal_salida.envia([self.id_nodo,visitados,'GO()'],[k])
                    self.hijos.append(k)

    
    def contiene (self, vecinos, visitados):
    # Verifica si la lista a es una sublista de b
        return set(vecinos).issubset(visitados)
    
    def nk (self, vecinos):
        return min(vecinos)
