from time import time

from responsibility import *
#from responsibility.problems.drsc_fig1a import T
#from responsibility.problems.drsc_fig1b import T
from responsibility.problems.drsc_fig1c import T
#from responsibility.problems.drsc_fig1d import T
#from responsibility.problems.drsc_fig2a import T
#from responsibility.problems.drsc_fig2b import T
#from responsibility.problems.drsc_fig3 import T
#from responsibility.problems.drsc_fig5 import T
#from responsibility.problems.qrpc_fig3 import T
#from responsibility.problems.public_good_2_of_3 import *
#from responsibility.problems.repeated_public_good_2_of_3 import *

#from responsibility.problems.threshold_public_good import *
#T = threshold_public_good(4,2)

print(repr(T))


T.make_globals()

print(Max(T.get_likelihood(T.root, strategy=s, resolve=Min) for s in T.get_strategies(T.root, player=i)))

print(Max(T.get_likelihood(T.root, scenario=s, resolve=Min) for s in T.get_scenarios(T.root, player=i)))

print(T.get_guaranteed_likelihood(T.root))

exit()

#print(T.get_guaranteed_likelihood(T.root))
T.draw("/tmp/test.pdf", show=True)


sc_allD = Scenario("allD", current_node=vi, tr={
    S: D for S in T.named_information_sets.values() if S.player != i
})
sc_jCkD = Scenario("jCkD", current_node=vi, tr={
    S: (C if S.player == j else D) for S in T.named_information_sets.values() if S.player != i
})
st_iC = Strategy("iC", start=vi.information_set, ch={
    S: C for S in T.get_information_sets(i).values()
})

print(T.get_likelihood(T.root,sc_allD,Strategy("", start=vi.information_set, ch={}),resolve="max"))

exit()

start = time()
dist = T.get_outcome_distribution(sc_jCkD, st_iC)
print(dist)
print(time()-start, "sec.")

exit()

start = time()
print(len(list(T.get_scenarios(vi, player=i))))
print(np.mean([T.get_outcome_distribution(sc, st_iC).get(enough, 0) for sc in T.get_scenarios(vi, player=i)]))
print(time()-start, "sec.")

#profile.print_stats()


exit()

start = time()
print(sum(1 for _ in T.get_strategies(vi, player=i)))
print(np.mean([T.get_outcome_distribution(scenario=sc_jCkD, strategy=st).get(enough, 0) for st in T.get_strategies(vi, player=i)]))
print(time()-start, "sec.")

print(T._n_not_used_cache, T._n_used_cache)

T.make_globals()

print()

print(T.named_nodes)
print(T.named_players)
print(T.named_outcomes)
print(T.named_actions)
print(T.named_inner_nodes)
print(T.named_leaf_nodes)
print(T.named_possibility_nodes)
print(T.named_probability_nodes)
print(T.named_decision_nodes)
print(T.named_information_sets)

#print(v4_unknown_warming.information_set.named_nodes)
#print(w14_cooling_knowingly_prevented.history)


