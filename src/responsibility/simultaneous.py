from .core import _AbstractObject, hasname
from .nodes import *

def make_simultaneous_move (name, *args, players=None, information_sets=None, consequences=None):
    """Generate a combination of DecisionNodes representing a set of players 
    making a "simultaneous move", i.e., each one taking an action without knowing
    what actions the other take.
    @param players: iterable of players taking a simultaneous move
    @param information_sets: optional iterable of information sets the new nodes
           should be added to, in the same order as players
    @param consequences: dict of successor node keyed by action tuple, the
           latter in the same order as players
    @return: the DecisionNode of the first listed player.
    """
    try:
        players[0]
    except:
        assert 0==1, "players must be list-like and non-empty"
    k = len(players)
    assert k > 0, "players must not be empty"
    if information_sets is None: 
        information_sets = [None for pl in players]
    else:
        try:
            information_sets[0]
        except:
            assert 0==1, "information_sets must be list-like"
        assert len(information_sets) == k, "information_sets must be of same length as players"
    information_sets = tuple(
        information_sets[pos] if information_sets[pos] is not None
        else InformationSet("S_" + name + "_" + str(players[pos]))
        for pos in range(k)
    )
    assert isinstance(consequences, dict), "consequences must be dict"
    A = consequences.keys()
    for a in A:
        assert isinstance(a, tuple), "action combinations must be tuples"
        assert len(a) == k, "action combinations must be of same length as players"
    if len(players) == 1:
        return DeN(name, *args, 
                   pl=players[0], 
                   ins=information_sets[0], 
                   co={a[0]: v for a, v in consequences.items()})
    else:
        # action set of first player:
        A0 = {a[0] for a in A}
        # action combinations of remaining players:
        Arest = {a[1:] for a in A}
        for a0 in A0:
            assert {a[1:] for a in A if a[0]==a0} == Arest, "consequences must have a key for all possible action combinations of the players"
        # return a decision node for the first player, followed be recursively generated other decision nodes:
        return DeN(name, *args, 
                   pl=players[0], 
                   ins=information_sets[0], 
                   co={a0: make_simultaneous_move (
                            name + "_" + a0.name, 
                            *args, 
                            players=players[1:], 
                            information_sets=information_sets[1:], 
                            consequences={
                                arest: consequences[(a0,) + arest]
                                for arest in Arest
                            })
                       for a0 in A0})
