import pyAgrum as gum
import os

def cargar_estructura(archivo_estructura):
    bn = gum.BayesNet()
    nodos = {} 
    with open(archivo_estructura, 'r') as archivo:
        for linea in archivo:
            padre, hijo = linea.strip().split(" -> ")
            if padre not in nodos:
                nodos[padre] = bn.add(gum.LabelizedVariable(padre, f'{padre} ?', 2))
            if hijo not in nodos:
                nodos[hijo] = bn.add(gum.LabelizedVariable(hijo, f'{hijo} ?', 2))
            bn.addArc(nodos[padre], nodos[hijo])
    return bn

def mostrar_estructura(bn):
    for nodo in bn.nodes():
        padres = bn.parents(nodo)
        if len(padres) > 0:
            print(f'Nodo {bn.variable(nodo).name()} depende de: {[bn.variable(p).name() for p in padres]}')
        else:
            print(f'Nodo {bn.variable(nodo).name()} no tiene predecesores')

def crear_imagen_bn(bn, nombre_archivo_dot='bayesnet.dot', nombre_imagen='bayesProyecto.png'):
    with open(nombre_archivo_dot, 'w') as f:
        f.write(bn.toDot())

    os.system(f'dot -Tpng {nombre_archivo_dot} -o {nombre_imagen}')
    print(f"La imagen de la red Bayesiana ha sido generada como '{nombre_imagen}'.")

bn = cargar_estructura('estructura_red.txt')
mostrar_estructura(bn)
crear_imagen_bn(bn)
