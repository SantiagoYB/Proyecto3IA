#Esto es hecho con este video, es solo para ver como deberia quedar una red bayesiana en python
#https://www.youtube.com/watch?v=Cdee62uUWno

import pyAgrum as gum
import os

# aca se crea todo el modelo bayeasiano
bn = gum.BayesNet()
cl = bn.add(gum.LabelizedVariable('cl', 'cloudy ?', 2))
s, r, w = [bn.add(name, 2) for name in "srw"]
bn.addArc(cl, s)
bn.addArc(cl, r)
bn.addArc(r, w)
bn.addArc(s, w)
print(bn)

# esto es para q se muestre en formato dot (esto lo hace el man del video pero es medio feo)
with open("bayesnet.dot", "w") as f:
    f.write(bn.toDot())

print("Creado bayesnet.dot")

# esto es para q se muestre en imagen como se ve la red bayesiana
os.system('dot -Tpng bayesnet.dot -o bayesvideo.png')

# esto es para mostrar q se creo la imagen
print("La imagen de la red Bayesiana ha sido generada como 'bayesnet.png'.")

# aca se definen las distribuciones
bn.cpt(cl).fillWith([0.5, 0.5])
bn.cpt(s)[:] = [[0.5, 0.5], [0.9, 0.1]]
print("Distribución condicional de S dado CL=0:", bn.cpt(s)[0])
print("Distribución condicional de S dado CL=1:", bn.cpt(s)[1])

bn.cpt(r)[{'cl': 0}] = [0.8, 0.2]
bn.cpt(r)[{'cl': 1}] = [0.2, 0.8]

bn.cpt(w)[{'r': 0, 's': 0}] = [1, 0]
bn.cpt(w)[{'r': 0, 's': 1}] = [0.1, 0.9]
bn.cpt(w)[{'r': 1, 's': 0}] = [0.1, 0.9]
bn.cpt(w)[{'r': 1, 's': 1}] = [0.01, 0.99]

# de aca para abajo son las inferencias
ie = gum.LazyPropagation(bn)
ie.makeInference()

print("Posterior de W sin evidencia:", ie.posterior(w))

ie.setEvidence({'s': 1, 'cl': 0})
ie.makeInference()

print("Posterior de W con evidencia (s=1, cl=0):", ie.posterior(w))

ie.setEvidence({'s': 0, 'cl': 0})
ie.makeInference()

print("Posterior de W con evidencia (s=0, c=0):", ie.posterior(w))