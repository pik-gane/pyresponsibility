"""Fig. 1b from Heitzig & Hiller (2020) Degrees of individual and groupwise 
backward and forward responsibility in extensive-form games with ambiguity, 
and their application to social choice problems. ArXiv:2007.07352

drsc_fig1b:
•: j
├─╴dont_throw_stone╶─╴v1 (j_unobserved): i
│                     ├─╴dont_throw_stone╶─╴v3: window_undamaged ✔
│                     ╰─╴throw_stone╶─╴v4: window_damaged ✖
╰─╴throw_stone╶─╴v2 (j_unobserved): i
                 ├─╴dont_throw_stone╶─╴v5: window_damaged ✖
                 ╰─╴throw_stone╶─╴v6: window_damaged ✖
                 
Agents i, j may each throw a stone into a window, not seeing the other’s action.
"""

from ..__init__ import *

global_players("i", "j")

global_actions("throw_stone", "dont_throw_stone")

window_undamaged = Ou("window_undamaged", ac=True)
window_damaged = Ou("window_damaged", ac=False)

j_unobserved = InS("j_unobserved")

T = Tree("drsc_fig1b", 
        ro=DeN("", pl=j, co={ 
            dont_throw_stone: DeN("v1", pl=i, ins=j_unobserved, co={ 
                dont_throw_stone: OuN("v3", ou=window_undamaged),
                throw_stone: OuN("v4", ou=window_damaged) 
            }),
            throw_stone: DeN("v2", pl=i, ins=j_unobserved, co={ 
                dont_throw_stone: OuN("v5", ou=window_damaged),
                throw_stone: OuN("v6", ou=window_damaged) 
            })
        })
    )

T.make_globals()
