"""Variant of Fig. 2b from Heitzig & Hiller (2020) Degrees of individual and groupwise 
backward and forward responsibility in extensive-form games with ambiguity, 
and their application to social choice problems. ArXiv:2007.07352

Here the original possibility node at the root is replaced by a probability node: 


Stylized version of a decision problem related to climate change, used to study 
the effect of options to reduce ambiguity on responsibility. Humanity (agent i) 
must choose between heating up Earth or not, initially not knowing whether there 
is a risk of global warming or cooling, but being able to acquire this knowledge 
by learning and having a prior probability distribution over the two cases.
"""

from ..__init__ import *

global_symbols("p")

global_players("i")

global_actions("learn", "dont_learn", "heat", "dont_heat")

climate_ok = Ou("climate_ok", ac=True)
global_outcomes("too_warm", "too_cold", ac=False)

global_inss("unknown_risk", "unlearned_risk")

T = Tree("drsc_fig2b_prob", 
        ro=PrN("risk_type", pr={
            DeN("v1_risk_of_warming", pl=i, ins=unknown_risk, co={
                learn: DeN("v3_known_warming", pl=i, co={
                    dont_heat: OuN("v7_warming_knowingly_prevented", ou=climate_ok),
                    heat: OuN("v8_warming_knowingly_allowed", ou=too_warm)
                }),
                dont_learn: DeN("v4_unknown_warming", pl=i, ins=unlearned_risk, co={
                    dont_heat: OuN("v9_warming_unknowingly_prevented", ou=climate_ok),
                    heat: OuN("v10_warming_unknowingly_allowed", ou=too_warm)
                })
            }): p,
            DeN("v2_risk_of_cooling", pl=i, ins=unknown_risk, co={
                dont_learn: DeN("v5_unknown_cooling", pl=i, ins=unlearned_risk, co={
                    dont_heat: OuN("v11_cooling_unknowingly_allowed", ou=too_cold),
                    heat: OuN("v12_cooling_unknowingly_prevented", ou=climate_ok)
                }),
                learn: DeN("v6_known_cooling", pl=i, co={
                    dont_heat: OuN("v13_cooling_knowingly_allowed", ou=too_cold),
                    heat: OuN("v14_cooling_knowingly_prevented", ou=climate_ok)
                })
            }): 1 - p,
        })
    )

T.make_globals()
