import pyAgrum as gum
bn = gum.BayesNet()
print(bn)
cl=bn.add(gum.LabelizedVariable('cl','cloudy ?',2))
print(cl)
print(bn)
s,r,w= [bn.add(name,2)for name in "srw"]
print(s,r,w)
print(bn)
bn.addArc(cl,s)
bn.addArc(cl,r)
bn.addArc(r,w)
bn.addArc(s,w)
print(bn)
import pyAgrum.lib.notebook as gnb  
bn