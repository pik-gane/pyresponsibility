"""Fig. 1b from Heitzig & Hiller (2020) Degrees of individual and groupwise 
backward and forward responsibility in extensive-form games with ambiguity, 
and their application to social choice problems. ArXiv:2007.07352"""

from ..__init__ import *

i = Pl("i")

learn = Ac("learn")
dont_learn = Ac("dont_learn")
heat = Ac("heat")
dont_heat = Ac("dont_heat")

climate_ok = Ou("climate_ok", ac=True)
too_warm = Ou("too_warm", ac=False)
too_cold = Ou("too_cold", ac=False)

unknown_risk = InS("unknown_risk")
unlearned_risk = InS("unlearned_risk")

T = Tree("drsc_fig2b", 
        ro=PoN("risk_type", su={
            DeN("v1_risk_of_warming", pl=i, ins=unknown_risk, co={
                learn: DeN("v3_known_warming", pl=i, co={
                    dont_heat: OuN("w7_warming_knowingly_prevented", ou=climate_ok),
                    heat: OuN("w8_warming_knowingly_allowed", ou=too_warm)
                }),
                dont_learn: DeN("v4_unknown_warming", pl=i, ins=unlearned_risk, co={
                    dont_heat: OuN("w9_warming_unknowingly_prevented", ou=climate_ok),
                    heat: OuN("w10_warming_unknowingly_allowed", ou=too_warm)
                })
            }),
            DeN("v2_risk_of_cooling", pl=i, ins=unknown_risk, co={
                dont_learn: DeN("v5_unknown_cooling", pl=i, ins=unlearned_risk, co={
                    dont_heat: OuN("w11_cooling_unknowingly_allowed", ou=too_cold),
                    heat: OuN("w12_cooling_unknowingly_prevented", ou=climate_ok)
                }),
                learn: DeN("v6_known_cooling", pl=i, co={
                    dont_heat: OuN("w13_cooling_knowingly_allowed", ou=too_cold),
                    heat: OuN("w14_cooling_knowingly_prevented", ou=climate_ok)
                })
            }),
        })
    )

T.make_globals()
