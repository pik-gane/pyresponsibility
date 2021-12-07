"""Fig. 1a from Heitzig & Hiller (2020) Degrees of individual and groupwise 
backward and forward responsibility in extensive-form games with ambiguity, 
and their application to social choice problems. ArXiv:2007.07352

drsc_fig1a:
•
├─╴not loaded╶─╴v1 (unknown_load): i
│               ├─╴pass_╶─╴v3: lives ✔
│               ╰─╴shoot╶─╴v4: lives ✔
╰─╴loaded╶─╴v2 (unknown_load): i
            ├─╴pass_╶─╴v5: lives ✔
            ╰─╴shoot╶─╴v6: dies ✖

Agent i may shoot a prisoner, not knowing whether the gun was loaded (node v2) 
or not (v1), leading to the prisoner dead (node v6) or alive (v3, v4, v5).            
"""

from ..__init__ import *

global_players("i")

global_actions("pass_", "shoot")

lives = Ou("lives", ac=True)
dies = Ou("dies", ac=False)

unknown_load = InS("unknown_load")

T = Tree("drsc_fig1a", 
        ro=PoN("", su={ 
            ("not loaded", DeN("v1", pl=i, ins=unknown_load, co={ 
                pass_: OuN("v3", ou=lives),
                shoot: OuN("v4", ou=lives) 
            })),
            ("loaded", DeN("v2", pl=i, ins=unknown_load, co={ 
                pass_: OuN("v5", ou=lives),
                shoot: OuN("v6", ou=dies) 
            }))
        })
    )

T.make_globals()
