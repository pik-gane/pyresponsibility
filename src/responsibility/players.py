from .core import _AbstractObject


class Player (_AbstractObject):

    _c_symbols = ["i", "j"]

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

Gr = Group

