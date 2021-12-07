"""Fig. 1d from Heitzig & Hiller (2020) Degrees of individual and groupwise 
backward and forward responsibility in extensive-form games with ambiguity, 
and their application to social choice problems. ArXiv:2007.07352

drsc_fig1d:
v1: i
├─╴rescue╶─╴v3: lives ✔
╰─╴pass_╶─╴passed
           ├─╴p╶─╴v2: i
           │      ├─╴rescue╶─╴v4: lives ✔
           │      ╰─╴pass_╶─╴v5: dies ✖
           ╰─╴1 - p╶─╴v6: dies ✖

Agent i may rescue someone now or, with some probably, later.
"""

from ..__init__ import *

global_symbols("p")

global_players("i")

global_actions("rescue", "pass_")

lives = Ou("lives", ac=True)
dies = Ou("dies", ac=False)

T = Tree("drsc_fig1d", ro=DeN("v1", pl=i, co={ 
        rescue: OuN("v3", ou=lives), 
        pass_: PrN("passed", pr={ 
            DeN("v2", pl=i, co={
                rescue: OuN("v4", ou=lives),
                pass_: OuN("v5", ou=dies)
            }): p,
            OuN("v6", ou=dies): 1 - p
        })
    })
)

T.make_globals()

