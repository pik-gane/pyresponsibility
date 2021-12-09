from .core import _AbstractObject, hasname


class Outcome (_AbstractObject):
    """Represents an outcome attached to one or more outcome nodes,
    and states whether it is ethically acceptable"""

    _i_is_acceptable = None
    @property
    def is_acceptable(self):
        """bool"""
        return self._i_is_acceptable

    def __init__(self, name, **kwargs):
        self._a_nodes = set()
        super(Outcome, self).__init__(name, **kwargs)

    _a_nodes = None
    @property
    def nodes(self):
        """Set of DecisionNodes, each having its information_set=this"""
        return self._a_nodes

    def add_node(self, node):
        self._a_nodes.add(node)
        self.validate()
        
    def validate(self):
        assert isinstance(self.is_acceptable, bool)

    def __repr__(self):
        return (self.name + " " if hasname(self) else "") + ("✔" if self.is_acceptable else "✖")

Ou = Outcome
"""Abbreviation for Outcome"""

