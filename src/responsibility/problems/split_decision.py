"""Problem highlighting the issue of whether it should or should not make a 
difference whether a player took two different actions immediately after one another
or whether this is treated as having taken only one, "combined" action.
Responsibility functions based on individual actions (like PRFs) will likely
be affected by this difference, while RFs based on whole strategies might not.

In the lower branch of this tree, action "bc" is strictly worse (strictly
Pareto-dominated) by action a, so taking action bc should be assigned positive
backward-responsibility. In the upper branch however, this action is split into
two parts, first "b", then "c". In node "step1", "b" is not strictly dominated
by "a" since there is a scenario in which "b" performs better than "a" (namely
the scenario in which the player continues with "d"). So "b" might be acceptable.
After having taken "b", "c" is also not strictly dominated in node "step2", 
because in some scenario it would perform better than "d". 
So "c" might seem acceptable as well. The counterargument would be that if the 
player excuses taking "b" by promising to then take "d", then this should
render "c" unacceptable.

split_decision:
split_or_not
├─╴step1: i
│  ├─╴a╶─╴split_a
│  │      ├─╴0.3333333333333333╶─╴split_a_bad: bad ✖
│  │      ╰─╴0.6666666666666666╶─╴split_a_good: good ✔
│  ╰─╴b╶─╴step2: i
│         ├─╴c╶─╴split_bc
│         │      ├─╴0.6666666666666666╶─╴split_bc_bad: bad ✖
│         │      ╰─╴0.3333333333333333╶─╴split_bc_good: good ✔
│         ╰─╴d╶─╴split_bd
│                ├─╴split_bd_bad: bad ✖
│                ╰─╴split_bd_good: good ✔
╰─╴unsplit: i
   ├─╴a╶─╴unsplit_a
   │      ├─╴0.3333333333333333╶─╴unsplit_a_bad: bad ✖
   │      ╰─╴0.6666666666666666╶─╴unsplit_a_good: good ✔
   ├─╴bc╶─╴unsplit_bc
   │       ├─╴0.6666666666666666╶─╴unsplit_bc_bad: bad ✖
   │       ╰─╴0.3333333333333333╶─╴unsplit_bc_good: good ✔
   ╰─╴bd╶─╴unsplit_bd
           ├─╴unsplit_bd_bad: bad ✖
           ╰─╴unsplit_bd_good: good ✔
"""

from ..__init__ import *

global_players("i")

global_actions("a", "b", "c", "d", "bc", "bd")

global_outcomes("good", ac=True)
global_outcomes("bad", ac=False)

T = Tree("split_decision", ro=PoN("split_or_not", su={
    DeN("step1", pl=i, co={
        a: PrN("split_a", pr={
            OuN("split_a_bad", ou=bad): 1/3,
            OuN("split_a_good", ou=good): 2/3
        }),
        b: DeN("step2", pl=i, co={
            c: PrN("split_bc", pr={
                OuN("split_bc_bad", ou=bad): 2/3,
                OuN("split_bc_good", ou=good): 1/3
            }),
            d: PoN("split_bd", su={
                OuN("split_bd_bad", ou=bad),
                OuN("split_bd_good", ou=good)
            }),
        }),
    }),
    DeN("unsplit", pl=i, co={
        a: PrN("unsplit_a", pr={
            OuN("unsplit_a_bad", ou=bad): 1/3,
            OuN("unsplit_a_good", ou=good): 2/3
        }),
        bc: PrN("unsplit_bc", pr={
            OuN("unsplit_bc_bad", ou=bad): 2/3,
            OuN("unsplit_bc_good", ou=good): 1/3
        }),
        bd: PoN("unsplit_bd", su={
            OuN("unsplit_bd_bad", ou=bad),
            OuN("unsplit_bd_good", ou=good)
        }),
    }),
}))

T.make_globals()
