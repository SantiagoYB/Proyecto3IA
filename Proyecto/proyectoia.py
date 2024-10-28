# Proyecto/red_bayesiana.py
# Lo del pyAgrum está basado en el video: https://www.youtube.com/watch?v=Cdee62uUWno
#comando para correr  el codigo python -m Proyecto.proyectoia

from Proyecto.red_bayesiana import RedBayesiana  # Importación absoluta

if __name__ == "__main__":
    red = RedBayesiana()
    red.cargar_estructura('Proyecto/estructura_red.txt')
    red.cargar_tablas_probabilidad('Proyecto/tabla_probabilidad.txt')
    red.mostrar_tablas_probabilidad()

    # Mostrar opciones de nodos para la consulta
    print("\nNodos disponibles para la consulta y evidencia:")
    for nombre_nodo in red.nodos:
        print(f" - {nombre_nodo}")

    # Solicitar al usuario el nodo de consulta
    query = input("\nIntroduce el nombre del nodo para realizar la consulta: ")
    while query not in red.nodos:
        print("Nodo no válido. Selecciona uno de los nodos disponibles.")
        query = input("Introduce el nombre del nodo para realizar la consulta: ")

    evidencia = {}
    
    # Solicitar nodos de evidencia al usuario
    while True:
        nodo = input("\nIntroduce el nombre de un nodo de evidencia o escribe 'salir' para terminar: ")
        if nodo.lower() == 'salir':
            break
        if nodo in red.nodos:  # Verificar que el nodo existe en la red
            try:
                estado = int(input(f"Introduce el estado de '{nodo}' (0 o 1): "))
                if estado in [0, 1]:  # Asegurarse de que el estado sea válido
                    evidencia[nodo] = estado
                else:
                    print("Estado inválido. Solo se permiten los valores 0 o 1.")
            except ValueError:
                print("Entrada inválida. Introduce un número entero (0 o 1).")
        else:
            print(f"El nodo '{nodo}' no existe en la red. Intenta con otro.")

    # Realizar inferencia sólo si el nodo de consulta existe en la red
    resultado = red.inferir_por_enumeracion(query, evidencia)
    print(f"\nProbabilidad de '{query}' dada la evidencia {evidencia}: {resultado}")
