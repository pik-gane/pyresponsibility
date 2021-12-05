import sys

from .core import _AbstractObject, hasname


class Player (_AbstractObject):

    _c_symbols = ["i", "j"]

    def __repr__(self):
        return self.name if hasname(self) else "~"

Pl = Player
    

class Group (_AbstractObject):

    _c_symbols = ["G", "H"]
    
    _i_players = None
    @property
    def players(self):
        """Set of member Players"""
        return self._i_players
    
    def validate(self):
        assert isinstance(self.players, set)
        for player in self.players:
            assert isinstance(player, Player), "group must be set of Players"
            
    def __contains__(self, player):
        return player in self.players
        
    def __repr__(self):
        return self.name if hasname(self) else "{*}"
        

Gr = Group

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
