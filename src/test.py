from responsibility import *
from responsibility.rfs.prfs.aafra import *
from responsibility.rfs.prfs.cooperation_oriented import *
from responsibility.rfs.prfs.domination_based import *
from responsibility.rfs.frfs import frf_from_max_prf

case = "split_decision_step1"
#case = "drsc_fig2b_prob_v1"

prfs = [r_like, r_like_KSym, r_risk, r_negl, r_coop, r_stbr]

subs = {}
if case == "random":
    T = random_tree(n_players=3, n_leafs=20)
    T.make_globals()
    v = [*T.get_decision_nodes([*T.players][0])][0]
if case == "random_mc":
    sums = {prf.name: 0 for prf in prfs}
    nits = 100
    for it in range(nits):
        T = random_tree(n_players=3, n_leafs=50)
        pl = [*T.players][0]
        G = Group("", players={pl})
        v = [*T.get_decision_nodes(pl)][0]        
        a = [*v.actions][0]
        for prf in prfs:
            sums[prf.name] += prf(tree=T, group=G, node=v, action=a)
    for prf in prfs:
        print(prf, sums[prf.name]/nits)
    exit()
if case == "split_decision_step1":
    from responsibility.problems.split_decision import T
    T.make_globals()
    v = step1
if case == "split_decision_step2":
    from responsibility.problems.split_decision import T
    T.make_globals()
    v = step2
if case == "split_decision_unsplit":
    from responsibility.problems.split_decision import T
    T.make_globals()
    v = unsplit
if case == "drsc_fig1a":
    from responsibility.problems.drsc_fig1a import T
    T.make_globals()
    v = v1
if case == "drsc_fig1bi":
    from responsibility.problems.drsc_fig1b import T
    T.make_globals()
    v = v2
    # that i gets blamed even if she does not throw in v2 shows that r_like is not plausible
if case == "drsc_fig1bj":
    from responsibility.problems.drsc_fig1b import T
    T.make_globals()
    v = T.root
if case == "drsc_fig1c":
    from responsibility.problems.drsc_fig1c import T
    T.make_globals()
    subs = {p: 0.8, q: 0.5}
    T = T.clone(subs=subs)
    T.make_globals(overwrite=True)
    v = v1
if case == "drsc_fig1d":
    from responsibility.problems.drsc_fig1d import T
    T.make_globals()
    subs = {p: 0.8}
    T = T.clone(subs=subs)
    T.make_globals(overwrite=True)
    v = v1
if case == "drsc_fig2bv1":
    # this case is only assessed correctly by r_stbr!
    from responsibility.problems.drsc_fig2b import T
    T.make_globals()
    v = v1_risk_of_warming
if case == "drsc_fig2bv4":
    # this case is only assessed correctly by r_stbr and r_negl.
    from responsibility.problems.drsc_fig2b import T
    T.make_globals()
    v = v4_unknown_warming
if case == "drsc_fig2b_prob_v1":
    # this case is only assessed correctly by r_stbr!
    from responsibility.problems.drsc_fig2b_prob import T
    T.make_globals()
    v = v1_risk_of_warming
if case == "drsc_fig2b_prob_v3":
    # this case is only assessed correctly by r_stbr!
    from responsibility.problems.drsc_fig2b_prob import T
    T.make_globals()
    v = v3_known_warming
if case == "qrpc_fig3":
    from responsibility.problems.qrpc_fig3 import T
    T.make_globals()
    subs = {p: 0.5}
    T = T.clone(subs=subs)
    T.make_globals(overwrite=True)
    v = root
if case == "forward_trust_v1":
    # this case is assessed wrongly by r_negl.
    from responsibility.problems.forward_trust import T
    T.make_globals()
    v = v1
if case == "forward_trust_v2":
    from responsibility.problems.forward_trust import T
    T.make_globals()
    v = v2
if case == "public_good_2_of_3":
    from responsibility.problems.public_good_2_of_3 import T
    T.make_globals()
    v = v1_contribute_contribute
if case == "coordination":
    from responsibility.problems.coordination import T
    T.make_globals()
    v = v1
       
#from responsibility.problems.drsc_fig1c import T
#from responsibility.problems.drsc_fig1d import T
#from responsibility.problems.drsc_fig2a import T
#from responsibility.problems.drsc_fig2b import T
#from responsibility.problems.drsc_fig3 import T
#from responsibility.problems.drsc_fig5 import T
#from responsibility.problems.qrpc_fig3 import T
#from responsibility.problems.public_good_2_of_3 import T
#from responsibility.problems.repeated_public_good_2_of_3 import *

#from responsibility.problems.threshold_public_good import *
#T = threshold_public_good(4, 2)


pl = v.player
G = Group("", players={pl})

T2 = tbrt(T, v.ins)
print("\n"+repr(T))
#print("\n"+repr(T2))

T.draw("/tmp/T.pdf", show=True)
T2.draw("/tmp/T2.pdf", show=True)


for prf in prfs:
    frf = frf_from_max_prf("", prf=prf)
    print(prf.name, ":")
    for a in v.actions:
        print(" ", {v2.name: prf(tree=T, group=G, node=v2, action=a) for v2 in v.information_set.nodes}, pl, a)
    print(" ", {v2.name: frf(tree=T, group=G, node=v2) for v2 in v.information_set.nodes}, pl, "FRF")
    
exit()



i=i1

print(Max([T.get_likelihood(T.root, strategy=s, resolve=Min) for s in T.get_strategies(T.root, player=i)]))

print(Max([T.get_likelihood(T.root, scenario=s, resolve=Min) for s in T.get_scenarios(T.root, player=i)]))

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

from time import time

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


