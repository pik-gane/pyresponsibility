"""Fig. 1b from Heitzig & Hiller (2020) Degrees of individual and groupwise 
backward and forward responsibility in extensive-form games with ambiguity, 
and their application to social choice problems. ArXiv:2007.07352"""

from ..__init__ import *

global_players("i", "j")

global_actions("throw_stone", "dont_throw_stone")

window_undamaged = Ou("window_undamaged", ac=True)
window_damaged = Ou("window_damaged", ac=False)

j_unobserved = InS("j_unobserved")

T = Tree("drsc_fig1a", 
        ro=DeN("", pl=j, co={ 
            dont_throw_stone: DeN("v1", pl=i, ins=j_unobserved, co={ 
                dont_throw_stone: OuN("w3", ou=window_undamaged),
                throw_stone: OuN("w4", ou=window_damaged) 
            }),
            throw_stone: DeN("v2", pl=i, ins=j_unobserved, co={ 
                dont_throw_stone: OuN("w5", ou=window_damaged),
                throw_stone: OuN("w6", ou=window_damaged) 
            })
        })
    )

T.make_globals()
