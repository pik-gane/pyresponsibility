"""Fig. 1c from Heitzig & Hiller (2020) Degrees of individual and groupwise 
backward and forward responsibility in extensive-form games with ambiguity, 
and their application to social choice problems. ArXiv:2007.07352"""

from ..__init__ import *

global_symbols("p", "q")

global_players("i")

global_actions("choose_p", "choose_q")

desired = Ou("desired", ac=True)
undesired = Ou("undesired", ac=False)

T = Tree("drsc_fig1c", ro=DeN("v1", pl=i, co={ 
        choose_p: PrN("chose_p", pr={ 
            OuN("w2", ou=desired): 1-p,
            OuN("w3", ou=undesired): p
        }), 
        choose_q: PrN("chose_q", pr={ 
            OuN("w4", ou=desired): 1-q,
            OuN("w5", ou=undesired): q
        })
    })
)

T.make_globals()
