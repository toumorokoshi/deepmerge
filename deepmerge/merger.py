from .strategy.value import ValueStrategies
from .strategy.list import ListStrategies
from .strategy.dict import DictStrategies
from .strategy.type_conflict import TypeConflictStrategies


class Merger(object):

    def __init__(self,
                 value_strategies,
                 list_strategies,
                 dict_strategies,
                 type_conflict_strategies):
        self._value_strategy = ValueStrategies(value_strategies)
        self._list_strategy = ListStrategies(list_strategies)
        self._dict_strategy = DictStrategies(dict_strategies)
        self._type_conflict_strategy = TypeConflictStrategies(
            type_conflict_strategies
        )

    def merge(self, base, nxt):
        return self.value_strategy(self, [], base, nxt)

    def value_strategy(self, *args):
        return self._value_strategy(*args)

    def list_strategy(self, *args):
        return self._list_strategy(*args)

    def dict_strategy(self, *args):
        return self._dict_strategy(self, *args)

    def type_conflict_strategy(self, *args):
        return self._type_conflict_strategy(self, *args)
