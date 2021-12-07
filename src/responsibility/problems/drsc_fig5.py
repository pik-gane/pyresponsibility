"""Fig. 5 from Heitzig & Hiller (2020) Degrees of individual and groupwise 
backward and forward responsibility in extensive-form games with ambiguity, 
and their application to social choice problems. ArXiv:2007.07352

drsc_fig5:
v1: i
├─╴choose_unknown╶─╴chose_unknown
│                   ├─╴w2: desired ✔
│                   ╰─╴w3: undesired ✖
╰─╴choose_p╶─╴chose_p
              ├─╴1 - p╶─╴w4: desired ✔
              ╰─╴p╶─╴w5: undesired ✖
              
Situation related to ambiguity aversion in which the complementarity of 
variants 1 and 2 of our responsibility functions can be seen. The agent must 
choose between an ambiguous course and a risky course. The ambiguous course 
seems the right choice in variant 1 since it does not increase the guaranteed 
likelihood of a bad outcome, which remains zero, while the risky course seems 
right in variant 2 since it reduces the minimax likelihood of a bad outcome 
from 1 to p.
"""

from ..__init__ import *

global_symbols("p")

global_players("i")

global_actions("choose_p", "choose_unknown")

desired = Ou("desired", ac=True)
undesired = Ou("undesired", ac=False)

T = Tree("drsc_fig5", ro=DeN("v1", pl=i, co={ 
        choose_unknown: PoN("chose_unknown", su={ 
            OuN("w2", ou=desired),
            OuN("w3", ou=undesired)
        }), 
        choose_p: PrN("chose_p", pr={ 
            OuN("w4", ou=desired): 1-p,
            OuN("w5", ou=undesired): p
        })
    })
)

T.make_globals()
