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
        self.value_strategy = ValueStrategies(value_strategies)
        self.list_strategy = ListStrategies(list_strategies)
        self.dict_strategy = DictStrategies(dict_strategies)
        self.type_conflict_strategy = TypeConflictStrategies(
            type_conflict_strategies
        )

    def merge(self, base, nxt):
        return self.value_strategy(self, [], base, nxt)


always_merger = Merger()
always_exception = Merger()
