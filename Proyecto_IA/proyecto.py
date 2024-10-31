import numpy as np

class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.predecesores = []
        self.probabilidades = {}

    def agregar_predecesor(self, nodo):
        self.predecesores.append(nodo)

    def set_probabilidad(self, estado, prob_verdad, prob_falso):
        self.probabilidades[estado] = (float(prob_verdad), float(prob_falso))

    def get_probabilidad(self, estado, verdad=True):
        if estado in self.probabilidades:
            return self.probabilidades[estado][0] if verdad else self.probabilidades[estado][1]
        return None

    def __str__(self):
        predecesores = ", ".join(pre.nombre for pre in self.predecesores)
        predecesores_str = f"[{predecesores}]" if predecesores else "[]"
        
        prob_str = "\n".join(f"    - {estado}: P(verdad) = {p[0]}, P(falso) = {p[1]}" for estado, p in self.probabilidades.items())
        
        return f"\n─────────────────────────────\nNodo: {self.nombre}\nPredecesores: {predecesores_str}\nProbabilidades:\n{prob_str if prob_str else '    No se han asignado probabilidades.'}"


class Grafo:
    def __init__(self):
        self.nodos = {}

    def agregar_nodo(self, nodo):
        self.nodos[nodo.nombre] = nodo

    def obtener_nodo(self, nombre):
        return self.nodos.get(nombre)

    def mostrar_estructura(self):
        print("\n=== Estructura de la Red Bayesiana ===")
        for nombre, nodo in self.nodos.items():
            print(nodo)
        print("─────────────────────────────")
        print("=== Fin de la Estructura ===\n")


def cargar_red_desde_archivo(nombre_archivo):
    grafo = Grafo()
    dependencias = {}
    seccion = None

    with open(nombre_archivo, "r") as file:
        for line in file:
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue
            
            if line == "DEPENDENCIAS":
                seccion = "DEPENDENCIAS"
                continue
            elif line == "PROBABILIDADES":
                seccion = "PROBABILIDADES"
                continue
            
            if seccion == "DEPENDENCIAS":
                nombre, *preds = line.replace(" ", "").split(":")
                nodo = Nodo(nombre)
                grafo.agregar_nodo(nodo)
                dependencias[nombre] = preds[0].split(",") if preds else []

            elif seccion == "PROBABILIDADES":
                nombre, estados = line.split("=", 1)
                nombre = nombre.strip()
                nodo = grafo.obtener_nodo(nombre)
                
                if nodo:
                    estado, valores = estados.split(":", 1)
                    prob_verdad, prob_falso = valores.split(",")
                    nodo.set_probabilidad(estado.strip(), prob_verdad.strip(), prob_falso.strip())

    for nombre, preds in dependencias.items():
        nodo = grafo.obtener_nodo(nombre)
        for pred in preds:
            pred_nodo = grafo.obtener_nodo(pred.strip())
            if pred_nodo:
                nodo.agregar_predecesor(pred_nodo)
    
    return grafo


def inferencia_por_enumeracion(grafo):
    respuesta = input("¿Qué desea saber? 'si' o 'no': ").strip().lower()
    es_verdad = True if respuesta == 'si' else False
    
    probabilidades = []
    for nombre, nodo in grafo.nodos.items():
        # Mostrar los estados posibles para el nodo
        estados_disponibles = ", ".join(nodo.probabilidades.keys())
        print(f"\nDigite el estado del nodo '{nombre}' (opciones: {estados_disponibles}):")
        
        estado = input(f"Estado para '{nombre}': ").strip().lower()
        prob = nodo.get_probabilidad(estado, es_verdad)
        
        if prob is not None:
            probabilidades.append(prob)
        else:
            print(f"Estado '{estado}' no encontrado para el nodo '{nombre}'. Intente con uno de los siguientes: {estados_disponibles}")

    resultado = np.prod(probabilidades)
    print(f"\nLa probabilidad de que ocurra el evento es: {resultado}")
    return resultado

grafo = cargar_red_desde_archivo("Proyecto_IA/red_bayesiana.txt")
grafo.mostrar_estructura()

resultado = inferencia_por_enumeracion(grafo)
print("\nResultado de la inferencia:", resultado)
