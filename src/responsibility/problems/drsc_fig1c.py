"""Fig. 1c from Heitzig & Hiller (2020) Degrees of individual and groupwise 
backward and forward responsibility in extensive-form games with ambiguity, 
and their application to social choice problems. ArXiv:2007.07352

drsc_fig1c:
v1: i
├─╴choose_p╶─╴chose_p
│             ├─╴1 - p╶─╴v2: desired ✔
│             ╰─╴p╶─╴v3: undesired ✖
╰─╴choose_q╶─╴chose_q
              ├─╴1 - q╶─╴v4: desired ✔
              ╰─╴q╶─╴v5: undesired ✖

Agent i can choose between two probabilities of an undesired outcome.
"""

from ..__init__ import *

global_symbols("p", "q")

global_players("i")

global_actions("choose_p", "choose_q")

desired = Ou("desired", ac=True)
undesired = Ou("undesired", ac=False)

T = Tree("drsc_fig1c", ro=DeN("v1", pl=i, co={ 
        choose_p: PrN("chose_p", pr={ 
            OuN("v2", ou=desired): 1-p,
            OuN("v3", ou=undesired): p
        }), 
        choose_q: PrN("chose_q", pr={ 
            OuN("v4", ou=desired): 1-q,
            OuN("v5", ou=undesired): q
        })
    })
)

T.make_globals()
