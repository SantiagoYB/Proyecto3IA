# Proyecto/nodo.py

import pyAgrum as gum

class Nodo:
    def __init__(self, nombre, variable):
        self.nombre = nombre
        self.variable = variable
        self.tabla_probabilidad = {}  # Tabla de probabilidad condicional (CPT)

    def establecer_tabla_probabilidad(self, tabla):
        self.tabla_probabilidad = tabla
