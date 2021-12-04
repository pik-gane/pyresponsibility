from ..__init__ import *

from sympy import symbols

p = symbols("p")

i = Pl("i")
a = Ac("a")
b = Ac("b")

good = Ou("good", ac=True)
bad = Ou("bad", ac=False)

w1 = OuN("w1", ou=bad)
w2 = OuN("w2", ou=good)
w3 = OuN("w3", ou=bad)
w4 = OuN("w4", ou=good)

v1 = PoN("v1", su={ w1, w2 })
v2 = PrN("v2", pr={ w3: p, w4: 1 - p })

r = DeN("r", pl=i, co={ a: v1, b: v2 })

tree = r.tree
