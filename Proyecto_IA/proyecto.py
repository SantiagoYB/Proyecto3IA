# Importa la biblioteca numpy para operaciones numéricas, especialmente el producto de probabilidades.
import numpy as np

# Define la clase Nodo para representar nodos en un grafo probabilístico.
class Nodo:
    # Método inicializador de la clase Nodo que recibe el nombre del nodo.
    def __init__(self, nombre):
        # Asigna el nombre del nodo.
        self.nombre = nombre
        # Inicializa una lista vacía para almacenar los predecesores del nodo.
        self.predecesores = []
        # Inicializa un diccionario vacío para almacenar las probabilidades condicionales del nodo.
        self.probabilidades = {}

    # Método para agregar un nodo predecesor a la lista de predecesores.
    def agregar_predecesor(self, nodo):
        self.predecesores.append(nodo)

    # Método para establecer la probabilidad de un estado dado en el nodo.
    def set_probabilidad(self, estado, prob_verdad, prob_falso):
        # Almacena las probabilidades de verdad y falso para el estado especificado.
        self.probabilidades[estado] = (float(prob_verdad), float(prob_falso))

    # Método para obtener la probabilidad de un estado dado en función de un valor de verdad o falso.
    def get_probabilidad(self, estado, verdad=True):
        # Si el estado está en las probabilidades, devuelve la probabilidad correspondiente.
        if estado in self.probabilidades:
            return self.probabilidades[estado][0] if verdad else self.probabilidades[estado][1]
        # Devuelve None si el estado no se encuentra.
        return None

    # Método para representar el nodo como una cadena, mostrando predecesores y probabilidades.
    def __str__(self):
        # Convierte la lista de predecesores en una cadena de nombres.
        predecesores = ", ".join(pre.nombre for pre in self.predecesores)
        # Formatea la lista de predecesores.
        predecesores_str = f"[{predecesores}]" if predecesores else "[]"
        
        # Genera una cadena con los estados y sus probabilidades.
        prob_str = "\n".join(f"    - {estado}: P(verdad) = {p[0]}, P(falso) = {p[1]}" for estado, p in self.probabilidades.items())
        
        # Devuelve una cadena con la información del nodo.
        return f"\n─────────────────────────────\nNodo: {self.nombre}\nPredecesores: {predecesores_str}\nProbabilidades:\n{prob_str if prob_str else '    No se han asignado probabilidades.'}"


# Define la clase Grafo para almacenar y manejar una colección de nodos.
class Grafo:
    # Inicializa un grafo vacío con un diccionario para almacenar nodos.
    def __init__(self):
        self.nodos = {}

    # Método para agregar un nodo al grafo.
    def agregar_nodo(self, nodo):
        self.nodos[nodo.nombre] = nodo

    # Método para obtener un nodo por su nombre.
    def obtener_nodo(self, nombre):
        return self.nodos.get(nombre)

    # Método para mostrar la estructura completa del grafo, incluyendo todos los nodos y sus probabilidades.
    def mostrar_estructura(self):
        print("\n=== Estructura de la Red Bayesiana ===")
        for nombre, nodo in self.nodos.items():
            print(nodo)
        print("─────────────────────────────")
        print("=== Fin de la Estructura ===\n")


# Función para cargar una red bayesiana desde un archivo de texto.
def cargar_red_desde_archivo(nombre_archivo):
    # Crea un nuevo grafo.
    grafo = Grafo()
    # Diccionario para almacenar dependencias entre nodos.
    dependencias = {}
    # Variable para identificar la sección actual en el archivo.
    seccion = None

    # Abre el archivo de red en modo lectura.
    with open(nombre_archivo, "r") as file:
        # Lee cada línea del archivo.
        for line in file:
            # Elimina espacios en blanco.
            line = line.strip()
            # Omite líneas vacías o comentarios.
            if line == "" or line.startswith("#"):
                continue
            
            # Verifica si la línea define la sección de dependencias.
            if line == "DEPENDENCIAS":
                seccion = "DEPENDENCIAS"
                continue
            # Verifica si la línea define la sección de probabilidades.
            elif line == "PROBABILIDADES":
                seccion = "PROBABILIDADES"
                continue
            
            # Procesa dependencias de nodos en la sección correspondiente.
            if seccion == "DEPENDENCIAS":
                nombre, *preds = line.replace(" ", "").split(":")
                nodo = Nodo(nombre)
                grafo.agregar_nodo(nodo)
                dependencias[nombre] = preds[0].split(",") if preds else []

            # Procesa probabilidades de nodos en la sección correspondiente.
            elif seccion == "PROBABILIDADES":
                nombre, estados = line.split("=", 1)
                nombre = nombre.strip()
                nodo = grafo.obtener_nodo(nombre)
                
                if nodo:
                    estado, valores = estados.split(":", 1)
                    prob_verdad, prob_falso = valores.split(",")
                    nodo.set_probabilidad(estado.strip(), prob_verdad.strip(), prob_falso.strip())

    # Asocia predecesores a cada nodo en el grafo según las dependencias.
    for nombre, preds in dependencias.items():
        nodo = grafo.obtener_nodo(nombre)
        for pred in preds:
            pred_nodo = grafo.obtener_nodo(pred.strip())
            if pred_nodo:
                nodo.agregar_predecesor(pred_nodo)
    
    # Devuelve el grafo cargado.
    return grafo


# Función para realizar inferencia por enumeración sobre el grafo.
def inferencia_por_enumeracion(grafo):
    # Pregunta al usuario sobre el evento a inferir.
    respuesta = input("¿Qué desea saber? 'si' o 'no': ").strip().lower()
    es_verdad = True if respuesta == 'si' else False
    
    # Inicializa una lista para almacenar probabilidades.
    probabilidades = []
    for nombre, nodo in grafo.nodos.items():
        # Muestra los estados posibles para cada nodo.
        estados_disponibles = ", ".join(nodo.probabilidades.keys())
        print(f"\nDigite el estado del nodo '{nombre}' (opciones: {estados_disponibles}):")
        
        # Solicita al usuario el estado para el nodo.
        estado = input(f"Estado para '{nombre}': ").strip().lower()
        # Obtiene la probabilidad del estado dado y si es verdad o falso.
        prob = nodo.get_probabilidad(estado, es_verdad)
        
        # Si la probabilidad existe, se añade a la lista; de lo contrario, se notifica al usuario.
        if prob is not None:
            probabilidades.append(prob)
        else:
            print(f"Estado '{estado}' no encontrado para el nodo '{nombre}'. Intente con uno de los siguientes: {estados_disponibles}")

    # Calcula el producto de todas las probabilidades.
    resultado = np.prod(probabilidades)
    print(f"\nLa probabilidad de que ocurra el evento es: {resultado}")
    # Devuelve el resultado de la inferencia.
    return resultado

# Carga el grafo desde un archivo y muestra su estructura.
grafo = cargar_red_desde_archivo("Proyecto_IA/red_bayesiana.txt")
grafo.mostrar_estructura()

# Realiza la inferencia por enumeración en el grafo.
resultado = inferencia_por_enumeracion(grafo)
print("\nResultado de la inferencia:", resultado)
