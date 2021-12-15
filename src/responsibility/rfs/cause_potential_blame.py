"""
A set of RFs based on the distinction between 
1. being a *cause* for an event that has actually occurred,
2. contributing or having contributed to the *potential* for a bad outcome,
3. being to *blame* for ones past or potential future actions.
"""

from ..core import Min, Max
from ..functions BRF

"""
1. Causation:
=============

Let us call any subset of outcome nodes (e.g. all outcome nodes with bad outcomes)
a possible "result" (in probability theory, this would be called an "event").

Given a certain result, to what degree did the sequence of actions a player or 
group performed contribute to that result?

Since this is not about knowledge, it should be independent of any information sets.

Since we have to deal with probabilistic uncertainty, we choose to measure this
"causation" form of backward responsibility in units of probability.
We interpret "causation" as "having raised the probability".

But what is the reference point w.r.t. which this raise should be measured?

In the absence of nonprobabilistic uncertainty, we could treat future actions 
as probabilistic, using some plausible (subjective) prior probability distribution 
for them, so that both at a decision node and at any of its possible successor 
nodes the result would have a well-defined probability. 
The reference for measuring the partial raising of the probability by having
taken a certain action in a certain decision node could then be the probability
just before the action, and the "raise" would be the probability just after
the action minus this reference value. One could then sum up these partial raises
over all actions taken by the player or group. However, if there are probability
nodes between the decision nodes, this sum might become larger than one, which
seems unplausible.

An alternative to this "pointwise" approach could be a "holistic" approach based
on action sequences rather than individual actions. The reference probability 
would be the probability at the root node. The probability "caused" by using a 
certain action sequence of a player or group would be the conditional 
probability under the assumption that at all actually visited decision nodes of 
the player or group, they would do what they actually did. The amount by which
a certain action sequence would have raised the probability of the result would 
then be measured by the difference between this conditional probability and the 
reference probability. This could also be interpreted as the change in probability
when "learning" that the player or group has taken a certain sequence of actions
then "updating" ones "beliefs" from the "prior" given by the reference probability
to the "posterior" given by the corresponding conditional probability.

Both approaches however require that we assign "prior" probabilities to actions,
which we want to avoid since that seems to be impossible in an objective way
due to the assumed free will of the players, and when instead done in a
subjective way, would be too arbitrary and subject to debates to be of much use.
This approach might however still be useful in a more psychological assessment
of responsibility than our ethical assessment.

We take a different approach here, in which we first make a "scenario-dependent"
assessment, which we then aggregate into an overall (scenario-independent)
assessment.

For this, let us assume that both nature's and all other players' choices at
all possibility nodes and decision nodes other than those of the player or group
at hand are fixed in some way, which we call a "scenario". Then each possible 
combination of actions for the player or group at all their decision nodes
implies a well-defined result probability. 

Let us call such a combination a "plan". 
(Note that some but not all plans can be interpreted as "strategies".
While a plan is a mapping from decision nodes to actions, a strategy is a 
mappings from *information sets* to actions. So while a strategy specifies the
same action for all nodes in an information set, a plan might specify different
actions for different nodes in the same information set. Although a plan that 
is not a strategies cannot be implemented with certainty (since the player does
not know in which node in the information set she is), it can still be 
implemented if the player makes the correct guesses, which is why we consider 
it relevant here. In the parts dealing with blame, we will only consider
plans that are strategies) 

We thus define:
"""

def causation_prob(tree, group, scenario, plan):
    return tree.get_likelihood(tree.root, scenario, plan) 

"""
Lacking a different reference probability, we can now use the minimum of those 
scenario-and-plan-dependent probabilities over all plans as the reference 
probability in this scenario:
"""

def causation_refprob(tree, group, scenario): 
    return Min(causation_prob(tree, group, scenario, plan)
               for plan in tree.get_plans(tree.root, group))

"""
The scenario-dependent raise in probability due to a certain plan is then
given by the difference between the probability under that plan and the 
above reference probability: 
"""

def causation_deltaprob(tree, group, scenario, plan): 
    return (causation_prob(tree, group, scenario, plan)
            - causation_refprob(tree, group, scenario))

"""
This basically measures by how much the probability for the result was 
"larger than necessary" in this scenario.

If the actual plan applied by the player or group was known, one could now
use the above as a measure of how much the player or group has raised the 
probability if the assumed scenario was the real scenario. But the actual plan 
is typically not be completely known because only a certain sequence of actions 
was observed, and it is unknown what the player or group would have done in 
decision nodes they did not actually encounter, of which there are typically
some. In the spirit of the principle "in doubt for the accused", we can
solve this problem by taking the minimum over all plans that are compatible
with the observed choices:
"""

def causation_mindeltaprob(tree, group, scenario, bad_outcome_node):
    return Min(causation_deltaprob(tree, group, scenario, plan)
               for plan in tree.get_plans(
                        group, 
                        fixed_path = bad_outcome_node.path
                    )
               )

"""
If the actual scenario was known, one could now use the above as a measure of 
how much the player or group has actually raised the probability. But just like
the player's plan, also the actual scenario may not be known completely
because only a certain sequence of actions by nature and the other players was 
observed, and it is unknown what nature or the other players would have done in 
possibility nodes and decision nodes they did not actually encounter. 

We could deal with this by taking a "best-case" or a "worst-case" approach. 
In order to avoid excessive attribution of responsibility and be more consistent
with our approach to dealing with the unknown parts of the player's plan, 
we choose to use the "best-case" approach, again taking the min:
"""

def causation_minmindeltaprob(tree, group, bad_outcome_node):
    return Min(causation_mindeltaprob(tree, group, scenario, bad_outcome_node)
               for scenario in tree.get_scenarios(
                        group, 
                        fixed_path = bad_outcome_node.path
                    )
               )
               
"""
On this we can base a first backward responsibility function aiming at measuring
the pure "causation" form of responsibility, which is zero at non-bad outcome 
nodes (no bad result was caused) and between zero and one at bad-outcome nodes:
"""

def _brf_causation(T, G, v):
    return 0 if v.outcome.is_acceptable else causation_minmindeltaprob(T, G, v)

brf_causation = BRF("causation-only BRF", function=_brf_causation)


