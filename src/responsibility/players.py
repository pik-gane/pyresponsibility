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
    """Represents any subset of the set of players"""

    _i_players = None
    @property
    def players(self):
        """Set of member Players"""
        return self._i_players
    
    def validate(self):
        assert isinstance(self.players, frozenset)
        for player in self.players:
            assert isinstance(player, Player), "group must be set of Players"
            
    def __contains__(self, player):
        return player in self.players
        
    def __repr__(self):
        return self.name if hasname(self) else "{*}"
        
Gr = Group
"""Abbreviation for Group"""

def players(*names):
    """Return a Player for each name listed as an argument"""
    return (Player(name) for name in names)
    
def global_players(*names):
    """Create a Player for each name listed as an argument 
    and store it in a global variable of the same name"""
    module_name = list(sys._current_frames().values())[0].f_back.f_globals['__name__']
    module = sys.modules[module_name]
    for pl in players(*names):
        n = pl.name
        if getattr(module, n, pl) != pl:
            print("Warning: global var", n, "existed, did not overwrite it.")
        else:
            setattr(module, n, pl)
