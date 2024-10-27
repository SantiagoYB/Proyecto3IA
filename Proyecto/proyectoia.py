# Proyecto/proyectoia.py
# para correr el código usar: python -m Proyecto.proyectoia
# lo del pyAgrum está basado en el video: https://www.youtube.com/watch?v=Cdee62uUWno

from Proyecto.red_bayesiana import RedBayesiana  # Importación absoluta


if __name__ == "__main__":
    red = RedBayesiana()
    red.cargar_estructura('Proyecto/estructura_red.txt')
    red.cargar_tablas_probabilidad('Proyecto/tabla_probabilidad.txt')
    red.mostrar_tablas_probabilidad()

    query = 'alarm' 
    evidencia = {'earthquake': 1, 'burglary': 0}  
    resultado = red.inferir_por_enumeracion(query, evidencia)
    print(f"Probabilidad de '{query}' dada la evidencia {evidencia}: {resultado}")
