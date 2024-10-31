# Proyecto/red_bayesiana.py
# El uso de pyAgrum para manejar redes bayesianas está basado en el video: https://www.youtube.com/watch?v=Cdee62uUWno

# Importa pyAgrum para crear y manipular redes bayesianas.
import pyAgrum as gum
# Importa la clase Nodo del módulo nodo dentro del proyecto.
from Proyecto.nodo import Nodo  

# Define la clase RedBayesiana, que representa una red bayesiana con nodos y probabilidades.
class RedBayesiana:
    # Método inicializador que crea una red bayesiana vacía y un diccionario de nodos.
    def __init__(self):
        # Crea una instancia de una red bayesiana usando pyAgrum.
        self.bn = gum.BayesNet()  
        # Inicializa un diccionario vacío para almacenar los nodos.
        self.nodos = {}          

    # Método para cargar la estructura de la red a partir de un archivo.
    def cargar_estructura(self, archivo_estructura):
        # Abre el archivo de estructura de la red en modo lectura.
        with open(archivo_estructura, 'r') as archivo:
            # Lee cada línea del archivo, donde cada línea representa una relación padre -> hijo.
            for linea in archivo:
                # Separa los nombres del nodo padre y del nodo hijo.
                padre, hijo = linea.strip().split(" -> ")
                # Si el nodo padre no está en el diccionario de nodos, lo añade como un nuevo Nodo.
                if padre not in self.nodos:
                    self.nodos[padre] = Nodo(padre, self.bn.add(gum.LabelizedVariable(padre, f'{padre} ?', 2)))
                # Si el nodo hijo no está en el diccionario de nodos, lo añade como un nuevo Nodo.
                if hijo not in self.nodos:
                    self.nodos[hijo] = Nodo(hijo, self.bn.add(gum.LabelizedVariable(hijo, f'{hijo} ?', 2)))
                # Añade un arco en la red bayesiana entre el nodo padre y el nodo hijo.
                self.bn.addArc(self.nodos[padre].variable, self.nodos[hijo].variable)

    # Método para cargar tablas de probabilidad condicional desde un archivo.
    def cargar_tablas_probabilidad(self, archivo_tablas):
        # Abre el archivo de tablas de probabilidad en modo lectura.
        with open(archivo_tablas, 'r') as archivo:
            # Lee cada línea del archivo.
            for linea in archivo:
                # Elimina espacios en blanco y continúa si la línea está vacía o es un comentario.
                linea = linea.strip()
                if not linea or linea.startswith('#'):  
                    continue
                
                # Procesa la línea si contiene un nombre de nodo y valores de probabilidad.
                if ':' in linea:
                    # Separa el nombre del nodo y sus valores de probabilidad.
                    nombre_nodo, valores = linea.split(':')
                    nombre_nodo = nombre_nodo.strip()
                    valores = valores.strip()
                    
                    # Si el nodo no tiene condiciones previas, se considera una probabilidad marginal.
                    if '|' not in nombre_nodo: 
                        probabilidad = eval(valores)  # Evalúa la cadena para obtener la lista de probabilidades.
                        # Asigna los valores de probabilidad para los estados 0 y 1.
                        self.bn.cpt(self.nodos[nombre_nodo].variable)[0] = probabilidad[1]  
                        self.bn.cpt(self.nodos[nombre_nodo].variable)[1] = probabilidad[0]  
                    else: 
                        # Si tiene condiciones previas, separa el nodo y su condición.
                        nodo_y_condicion = nombre_nodo.split('|')
                        nombre_nodo = nodo_y_condicion[0].strip()
                        condicion = nodo_y_condicion[1].strip()
                        valores = eval(valores)
                        
                        # Crea un diccionario de condiciones a partir de la cadena de condición.
                        condiciones = {cond.split('=')[0]: int(cond.split('=')[1]) for cond in condicion.split(',')}
                        # Asigna las probabilidades condicionales a los estados específicos en la CPT.
                        for valor, prob in zip([0, 1], valores[::-1]):  
                            self.bn.cpt(self.nodos[nombre_nodo].variable)[valor, *condiciones.values()] = prob

    # Método para mostrar las tablas de probabilidad condicional para cada nodo.
    def mostrar_tablas_probabilidad(self):
        # Itera sobre cada nodo en el diccionario de nodos.
        for nodo in self.nodos.values():
            # Muestra el nombre del nodo y su tabla de probabilidad condicional.
            print(f"Tabla de probabilidad para el nodo {nodo.nombre}:")
            print(self.bn.cpt(nodo.variable))
            print()

    # Método para realizar inferencia por enumeración en la red bayesiana.
    def inferir_por_enumeracion(self, query, evidencia):
        # Crea un objeto LazyPropagation para realizar la inferencia.
        ie = gum.LazyPropagation(self.bn)  
        # Formatea la evidencia para que coincida con las variables en la red bayesiana.
        evidencia_formateada = {self.nodos[var].variable: estado for var, estado in evidencia.items()}
        # Establece la evidencia en el objeto de inferencia.
        ie.setEvidence(evidencia_formateada)  
        # Realiza la inferencia.
        ie.makeInference()  

        # Devuelve la probabilidad posterior del nodo de consulta dado la evidencia.
        return ie.posterior(self.nodos[query].variable)
