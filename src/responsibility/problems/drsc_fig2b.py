"""Fig. 2b from Heitzig & Hiller (2020) Degrees of individual and groupwise 
backward and forward responsibility in extensive-form games with ambiguity, 
and their application to social choice problems. ArXiv:2007.07352

drsc_fig2b:
risk_type
├─╴v1_risk_of_warming (unknown_risk): i
│  ├─╴learn╶─╴v3_known_warming: i
│  │          ├─╴dont_heat╶─╴v7_warming_knowingly_prevented: climate_ok ✔
│  │          ╰─╴heat╶─╴v8_warming_knowingly_allowed: too_warm ✖
│  ╰─╴dont_learn╶─╴v4_unknown_warming (unlearned_risk): i
│                  ├─╴dont_heat╶─╴v9_warming_unknowingly_prevented: climate_ok ✔
│                  ╰─╴heat╶─╴v10_warming_unknowingly_allowed: too_warm ✖
╰─╴v2_risk_of_cooling (unknown_risk): i
   ├─╴dont_learn╶─╴v5_unknown_cooling (unlearned_risk): i
   │               ├─╴dont_heat╶─╴v11_cooling_unknowingly_allowed: too_cold ✖
   │               ╰─╴heat╶─╴v12_cooling_unknowingly_prevented: climate_ok ✔
   ╰─╴learn╶─╴v6_known_cooling: i
              ├─╴dont_heat╶─╴v13_cooling_knowingly_allowed: too_cold ✖
              ╰─╴heat╶─╴v14_cooling_knowingly_prevented: climate_ok ✔

Stylized version of a decision problem related to climate change, used to study 
the effect of options to reduce ambiguity on responsibility. Humanity (agent i) 
must choose between heating up Earth or not, initially not knowing whether there 
is a risk of global warming or cooling, but being able to acquire this knowledge 
by learning.
"""

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
                    dont_heat: OuN("v7_warming_knowingly_prevented", ou=climate_ok),
                    heat: OuN("v8_warming_knowingly_allowed", ou=too_warm)
                }),
                dont_learn: DeN("v4_unknown_warming", pl=i, ins=unlearned_risk, co={
                    dont_heat: OuN("v9_warming_unknowingly_prevented", ou=climate_ok),
                    heat: OuN("v10_warming_unknowingly_allowed", ou=too_warm)
                })
            }),
            DeN("v2_risk_of_cooling", pl=i, ins=unknown_risk, co={
                dont_learn: DeN("v5_unknown_cooling", pl=i, ins=unlearned_risk, co={
                    dont_heat: OuN("v11_cooling_unknowingly_allowed", ou=too_cold),
                    heat: OuN("v12_cooling_unknowingly_prevented", ou=climate_ok)
                }),
                learn: DeN("v6_known_cooling", pl=i, co={
                    dont_heat: OuN("v13_cooling_knowingly_allowed", ou=too_cold),
                    heat: OuN("v14_cooling_knowingly_prevented", ou=climate_ok)
                })
            }),
        })
    )

T.make_globals()
