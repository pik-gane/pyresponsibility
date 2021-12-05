from .core import _AbstractObject, hasname


class Outcome (_AbstractObject):

    _c_symbols = ["o"]
    
    _i_is_acceptable = None
    @property
    def is_acceptable(self):
        """bool"""
        return self._i_is_acceptable

    def validate(self):
        assert isinstance(self.is_acceptable, bool)

    def __repr__(self):
        return (self.name + " " if hasname(self) else "") + ("✔" if self.is_acceptable else "✖")

Ou = Outcome

