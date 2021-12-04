from .core import _AbstractObject


class Outcome (_AbstractObject):

    _c_symbols = ["o"]
    
    _i_is_acceptable = None
    @property
    def is_acceptable(self):
        """bool"""
        return self._i_is_acceptable

    def validate(self):
        assert isinstance(self.is_acceptable, bool)

Ou = Outcome

