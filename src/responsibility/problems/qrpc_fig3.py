from ..__init__ import *

from sympy import symbols

global_symbols("p")

good = Ou("good", ac=True)
bad = Ou("bad", ac=False)

T = Tree("qrpc_fig3",
        ro=DeN("", pl=Pl("i"), co={ 
            Ac("a"): PoN("v1", su={ 
                OuN("w1", ou=bad), 
                OuN("w2", ou=good),
            }), 
            Ac("b"): PrN("v2", pr={ 
                OuN("w3", ou=bad): p, 
                OuN("w4", ou=good): 1 - p, 
            }),
        })
    )

T.make_globals()

