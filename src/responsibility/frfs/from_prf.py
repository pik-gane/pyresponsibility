from ..core import Max, Min
from ..functions import FRF, PRF

def frf_from_max_prf(name, desc=None, prf=None):
    """Constructs an FRF from a PRF by taking the maximum over all actions' 
    PRFs at the node."""
    assert isinstance(prf, PRF)
    return FRF(name, desc=desc, function=(
        lambda T, G, v: Max([prf(T, G, v, a) for a in v.actions])
    ))
    
def frf_from_max_ins_max_prf(name, desc=None, prf=None):
    """Constructs an FRF from a PRF by taking the maximum over all actions' 
    PRFs at any node in the node's information set."""
    assert isinstance(prf, PRF)
    return FRF(name, desc=desc, function=(
        lambda T, G, v: Max([prf(T, G, v2, a) 
                             for v2 in v.ins.nodes
                             for a in v2.actions])
    ))
    
def frf_from_maxdiff_prf(name, desc=None, prf=None):
    """Constructs an FRF from a PRF by taking the maximum difference between
    all actions' PRFs at the node."""
    assert isinstance(prf, PRF)
    def frf(T, G, v):
        values = [prf(T, G, v, a) for a in v.actions]
        return Max(values) - Min(values)
    return FRF(name, desc=desc, function=frf)

def frf_from_max_ins_maxdiff_prf(name, desc=None, prf=None):
    """Constructs an FRF from a PRF by taking the maximum difference between
    all actions' PRFs at any node in the node's information set."""
    assert isinstance(prf, PRF)
    def frf0(T, G, v):
        values = [prf(T, G, v, a) for a in v.actions]
        return Max(values) - Min(values)
    return FRF(name, desc=desc, function=(
        lambda T, G, v, a: Max([frf0(T, G, v2) for v2 in v.ins.nodes])
    ))
