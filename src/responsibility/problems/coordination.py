"""Coordination game used in Fig. 2 from Hiller, S., Israel, J., & Heitzig, J. (2021). An Axiomatic Approach to Formalized Responsibility Ascription.
"""

from ..__init__ import *

global_players("i", "j")

global_actions("cinema", "theater")

global_outcomes("meet", ac=True)
global_outcomes("dont_meet", ac=False)

T = Tree("coordination", ro=make_simultaneous_move("v1", players=(i, j),
       consequences={
           (cinema, cinema): OuN("w1", ou=meet),
           (cinema, theater): OuN("w2", ou=dont_meet),
           (theater, cinema): OuN("w3", ou=dont_meet),
           (theater, theater): OuN("w4", ou=meet),
       }))

T.make_globals()
