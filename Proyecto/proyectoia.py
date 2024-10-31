# Proyecto/red_bayesiana.py
# El uso de pyAgrum para manejar redes bayesianas está basado en el video de YouTube: https://www.youtube.com/watch?v=Cdee62uUWno
# Comando para ejecutar este archivo desde la línea de comandos: python -m Proyecto.proyectoia

# Importa la clase RedBayesiana desde el módulo red_bayesiana dentro del proyecto.
from Proyecto.red_bayesiana import RedBayesiana  

# Verifica si el script se está ejecutando directamente (no como un módulo importado).
if __name__ == "__main__":
    # Crea una instancia de la clase RedBayesiana.
    red = RedBayesiana()
    # Carga la estructura de la red desde un archivo de texto especificado.
    red.cargar_estructura('Proyecto/estructura_red.txt')
    # Carga las tablas de probabilidad desde un archivo de texto especificado.
    red.cargar_tablas_probabilidad('Proyecto/tabla_probabilidad.txt')
    # Muestra las tablas de probabilidad para todos los nodos de la red.
    red.mostrar_tablas_probabilidad()

    # Imprime un mensaje y muestra los nombres de los nodos que se pueden consultar o usar como evidencia.
    print("\nNodos disponibles para la consulta y evidencia:")
    # Recorre y muestra cada nombre de nodo en la red.
    for nombre_nodo in red.nodos:
        print(f" - {nombre_nodo}")

    # Solicita al usuario que introduzca el nombre de un nodo para hacer una consulta.
    query = input("\nIntroduce el nombre del nodo para realizar la consulta: ")
    # Repite la solicitud hasta que el usuario ingrese un nodo válido.
    while query not in red.nodos:
        print("Nodo no válido. Selecciona uno de los nodos disponibles.")
        query = input("Introduce el nombre del nodo para realizar la consulta: ")

    # Inicializa un diccionario vacío para almacenar los nodos de evidencia y sus estados.
    evidencia = {}
    
    # Bucle para permitir que el usuario introduzca varios nodos de evidencia.
    while True:
        # Pide el nombre de un nodo de evidencia o 'salir' para terminar.
        nodo = input("\nIntroduce el nombre de un nodo de evidencia o escribe 'salir' para terminar: ")
        # Si el usuario escribe 'salir', el bucle se interrumpe.
        if nodo.lower() == 'salir':
            break
        # Comprueba si el nodo ingresado existe en la red.
        if nodo in red.nodos:  
            try:
                # Solicita al usuario el estado (0 o 1) para el nodo de evidencia.
                estado = int(input(f"Introduce el estado de '{nodo}' (0 o 1): "))
                # Solo se aceptan los valores 0 o 1 como estados válidos.
                if estado in [0, 1]: 
                    # Añade el nodo y su estado al diccionario de evidencia.
                    evidencia[nodo] = estado
                else:
                    # Informa al usuario si el estado ingresado no es válido.
                    print("Estado inválido. Solo se permiten los valores 0 o 1.")
            except ValueError:
                # Informa al usuario si la entrada no es un número entero válido.
                print("Entrada inválida. Introduce un número entero (0 o 1).")
        else:
            # Informa al usuario si el nodo ingresado no existe en la red.
            print(f"El nodo '{nodo}' no existe en la red. Intenta con otro.")

    # Realiza una inferencia por enumeración en la red para calcular la probabilidad del nodo de consulta dado la evidencia.
    resultado = red.inferir_por_enumeracion(query, evidencia)
    # Muestra el resultado de la probabilidad calculada en pantalla.
    print(f"\nProbabilidad de '{query}' dada la evidencia {evidencia}: {resultado}")
