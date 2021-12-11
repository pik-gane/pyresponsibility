"""
forward_trust:
v0
├─╴v1: i
│  ├─╴C╶─╴v1C: j
│  │      ├─╴C╶─╴w1CC: good ✔
│  │      ╰─╴D╶─╴w1CD: good ✔
│  ╰─╴D╶─╴v1D: j
│         ├─╴C╶─╴w1DC: good ✔
│         ╰─╴D╶─╴w1DD: bad ✖
╰─╴v2: i
   ├─╴C╶─╴v2C (S2i): j
   │      ├─╴C╶─╴w2CC: good ✔
   │      ╰─╴D╶─╴w2CD: good ✔
   ╰─╴D╶─╴v2D (S2i): j
          ├─╴C╶─╴w2DC: good ✔
          ╰─╴D╶─╴w2DD: bad ✖
"""
from ..__init__ import *

from sympy import symbols

global_players("i", "j")
global_actions("C", "D")
global_outcomes("good", ac=True)
global_outcomes("bad", ac=False)

global_inss("S2i")

T = Tree("forward_trust", 
         ro=PoN("v0", su={
             DeN("v1", pl=i, co={
                 C: DeN("v1C", pl=j, co={
                     C: OuN("w1CC", ou=good),
                     D: OuN("w1CD", ou=good)
                 }),
                 D: DeN("v1D", pl=j, co={
                     C: OuN("w1DC", ou=good),
                     D: OuN("w1DD", ou=bad)
                 })
             }),
             DeN("v2", pl=i, co={
                 C: DeN("v2C", pl=j, ins=S2i, co={
                     C: OuN("w2CC", ou=good),
                     D: OuN("w2CD", ou=good)
                 }),
                 D: DeN("v2D", pl=j, ins=S2i, co={
                     C: OuN("w2DC", ou=good),
                     D: OuN("w2DD", ou=bad)
                 })
             })
         })
     )

T.make_globals()
