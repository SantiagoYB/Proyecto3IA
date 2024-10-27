# Proyecto/red_bayesiana.py
# Lo del pyAgrum está basado en el video: https://www.youtube.com/watch?v=Cdee62uUWno

import pyAgrum as gum
from Proyecto.nodo import Nodo  

class RedBayesiana:
    def __init__(self):
        self.bn = gum.BayesNet()  
        self.nodos = {}          

    def cargar_estructura(self, archivo_estructura):
        with open(archivo_estructura, 'r') as archivo:
            for linea in archivo:
                padre, hijo = linea.strip().split(" -> ")
                if padre not in self.nodos:
                    self.nodos[padre] = Nodo(padre, self.bn.add(gum.LabelizedVariable(padre, f'{padre} ?', 2)))
                if hijo not in self.nodos:
                    self.nodos[hijo] = Nodo(hijo, self.bn.add(gum.LabelizedVariable(hijo, f'{hijo} ?', 2)))
                self.bn.addArc(self.nodos[padre].variable, self.nodos[hijo].variable)

    def cargar_tablas_probabilidad(self, archivo_tablas):
        with open(archivo_tablas, 'r') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea or linea.startswith('#'):  
                    continue
                
                if ':' in linea:
                    nombre_nodo, valores = linea.split(':')
                    nombre_nodo = nombre_nodo.strip()
                    valores = valores.strip()
                    
                    if '|' not in nombre_nodo: 
                        probabilidad = eval(valores)  
                        self.bn.cpt(self.nodos[nombre_nodo].variable)[0] = probabilidad[1]  
                        self.bn.cpt(self.nodos[nombre_nodo].variable)[1] = probabilidad[0]  
                    else: 
                        nodo_y_condicion = nombre_nodo.split('|')
                        nombre_nodo = nodo_y_condicion[0].strip()
                        condicion = nodo_y_condicion[1].strip()
                        valores = eval(valores)
                        
                        condiciones = {cond.split('=')[0]: int(cond.split('=')[1]) for cond in condicion.split(',')}
                        for valor, prob in zip([0, 1], valores[::-1]):  
                            self.bn.cpt(self.nodos[nombre_nodo].variable)[valor, *condiciones.values()] = prob

    def mostrar_tablas_probabilidad(self):
        for nodo in self.nodos.values():
            print(f"Tabla de probabilidad para el nodo {nodo.nombre}:")
            print(self.bn.cpt(nodo.variable))
            print()

    def inferir_por_enumeracion(self, query, evidencia):
        ie = gum.LazyPropagation(self.bn)  
        evidencia_formateada = {self.nodos[var].variable: estado for var, estado in evidencia.items()}
        ie.setEvidence(evidencia_formateada)  
        ie.makeInference()  

        return ie.posterior(self.nodos[query].variable)
