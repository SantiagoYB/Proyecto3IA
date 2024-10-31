# Proyecto/nodo.py

# Importa la biblioteca pyAgrum para manejar redes bayesianas.
import pyAgrum as gum

# Define la clase Nodo, que representa un nodo en una red bayesiana.
class Nodo:
    # Método inicializador de la clase Nodo, que recibe un nombre y una variable.
    def __init__(self, nombre, variable):
        # Asigna el nombre del nodo.
        self.nombre = nombre
        # Asigna la variable del nodo.
        self.variable = variable
        # Inicializa un diccionario vacío para la tabla de probabilidad condicional (CPT).
        self.tabla_probabilidad = {}

    # Define un método para establecer la tabla de probabilidad condicional del nodo.
    def establecer_tabla_probabilidad(self, tabla):
        # Asigna el diccionario proporcionado como la tabla de probabilidad del nodo.
        self.tabla_probabilidad = tabla
