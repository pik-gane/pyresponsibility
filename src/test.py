from responsibility import *
from responsibility.problems.qrpc_fig3 import *

sc = Scenario("upper", anchor=r, tr={v1: w1})
st = Strategy("b", anchor=r, ch={r.information_set: b})

dist = tree.get_outcome_distribution(sc, st)
print(dist)

