"""Fig. 1a from Heitzig & Hiller (2020) Degrees of individual and groupwise 
backward and forward responsibility in extensive-form games with ambiguity, 
and their application to social choice problems. ArXiv:2007.07352"""

from ..__init__ import *

global_players("i")

global_actions("pass_", "shoot")

lives = Ou("lives", ac=True)
dies = Ou("dies", ac=False)

unknown_load = InS("unknown_load")

T = Tree("drsc_fig1a", 
        ro=PoN("", su={ 
            ("not loaded", DeN("v1", pl=i, ins=unknown_load, co={ 
                pass_: OuN("w3", ou=lives),
                shoot: OuN("w4", ou=lives) 
            })),
            ("loaded", DeN("v2", pl=i, ins=unknown_load, co={ 
                pass_: OuN("w5", ou=lives),
                shoot: OuN("w6", ou=dies) 
            }))
        })
    )

T.make_globals()
