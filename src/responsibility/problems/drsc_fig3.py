"""Fig. 3 from Heitzig & Hiller (2020) Degrees of individual and groupwise 
backward and forward responsibility in extensive-form games with ambiguity, 
and their application to social choice problems. ArXiv:2007.07352

drsc_fig3:
v1: i
├─╴dont_hesitate╶─╴w3: lives ✔
╰─╴hesitate╶─╴v2: i
              ├─╴try_after_all╶─╴delayed_try
              │                  ├─╴succeed╶─╴w4: lives ✔
              │                  ╰─╴fail╶─╴w6: dies ✖
              ╰─╴pass_╶─╴w5: dies ✖

Situation related to the Independence of Nested Decisions (IND) axiom. The agent 
sees someone having a heart attack and may either try to rescue them without 
hesitation, applying CPU until the ambulance arrives, or hesitate and then 
reconsider and try rescuing them after all, in which case it is ambiguous 
whether the attempt can still succeed.
"""

from ..__init__ import *

global_players("i")

global_actions("hesitate", "dont_hesitate", "try_after_all", "pass_")

lives = Ou("lives", ac=True)
dies = Ou("dies", ac=False)

T = Tree("drsc_fig3", ro=DeN("v1", pl=i, co={ 
        dont_hesitate: OuN("w3", ou=lives), 
        hesitate: DeN("v2", pl=i, co={
            try_after_all: PoN("delayed_try", su={
                ("succeed", OuN("w4", ou=lives)),
                ("fail", OuN("w6", ou=dies))
            }),
            pass_: OuN("w5", ou=dies)
        })
    })
)

T.make_globals()



