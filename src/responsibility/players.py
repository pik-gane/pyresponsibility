import sys

from .core import _AbstractObject, hasname


class Player (_AbstractObject):
    """Represents a player who can take one of several actions at one or more 
    decision nodes"""

    def __repr__(self):
        return self.name if hasname(self) else "~"

Pl = Player
"""Abbreviation for Player"""

class Group (_AbstractObject):
    """Represents any subset of the set of named_players"""

    _i_players = None
    @property
    def named_players(self):
        """Set of member Players"""
        return self._i_players
    
    def validate(self):
        assert isinstance(self.named_players, frozenset)
        for player in self.named_players:
            assert isinstance(player, Player), "group must be set of Players"
            
    def __contains__(self, player):
        return player in self.named_players
        
    def __repr__(self):
        return self.name if hasname(self) else "{*}"
        
Gr = Group
"""Abbreviation for Group"""

def named_players(*names):
    """Return a Player for each name listed as an argument"""
    return tuple(Player(name) for name in names)
    
def global_players(*names):
    """Create a Player for each name listed as an argument 
    and store it in a global variable of the same name"""
    module_name = list(sys._current_frames().values())[0].f_back.f_globals['__name__']
    module = sys.modules[module_name]
    for pl in named_players(*names):
        n = pl.name
        if getattr(module, n, pl) != pl:
            print("Warning: global var", n, "existed, did not overwrite it.")
        else:
            setattr(module, n, pl)
