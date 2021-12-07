"""Fig. 2a from Heitzig & Hiller (2020) Degrees of individual and groupwise 
backward and forward responsibility in extensive-form games with ambiguity, 
and their application to social choice problems. ArXiv:2007.07352

drsc_fig2a:
risk_type
├─╴cooling╶─╴v5_unknown_cooling (unknown_risk): i
│            ├─╴dont_heat╶─╴v11_cooling_unknowingly_allowed: too_cold ✖
│            ╰─╴heat╶─╴v12_cooling_unknowingly_prevented: climate_ok ✔
╰─╴warming╶─╴v4_unknown_warming (unknown_risk): i
             ├─╴dont_heat╶─╴v9_warming_unknowingly_prevented: climate_ok ✔
             ╰─╴heat╶─╴v10_warming_unknowingly_allowed: too_warm ✖
             
Stylized version of a decision problem related to climate change, used to study 
the effect of options to reduce ambiguity on responsibility. Humanity (agent i) 
must choose between heating up Earth or not, initially not knowing whether 
there is a risk of global warming or cooling.
"""

from ..__init__ import *

i = Pl("i")

heat = Ac("heat")
dont_heat = Ac("dont_heat")

climate_ok = Ou("climate_ok", ac=True)
too_warm = Ou("too_warm", ac=False)
too_cold = Ou("too_cold", ac=False)

unknown_risk = InS("unknown_risk")

T = Tree("drsc_fig2a", 
        ro=PoN("risk_type", su={
            ("warming", DeN("v4_unknown_warming", pl=i, ins=unknown_risk, co={
                dont_heat: OuN("v9_warming_unknowingly_prevented", ou=climate_ok),
                heat: OuN("v10_warming_unknowingly_allowed", ou=too_warm)
            })),
            ("cooling", DeN("v5_unknown_cooling", pl=i, ins=unknown_risk, co={
                dont_heat: OuN("v11_cooling_unknowingly_allowed", ou=too_cold),
                heat: OuN("v12_cooling_unknowingly_prevented", ou=climate_ok)
            }))
        })
    )

T.make_globals()
