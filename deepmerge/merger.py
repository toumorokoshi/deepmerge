from .strategy.value import VALUE_STRATEGIES
from .strategy.list import LIST_STRATEGIES
from .strategy.dict import DICT_STRATEGIES
from .strategy.type_conflict import TYPE_CONFLICT_STRATEGIES


class Merger(object):

    def __init__(self,
                 value_strategies,
                 list_strategies,
                 dict_strategies,
                 type_conflict_strategies):
        self._value_strategies = value_strategies
        self._
        pass

    def merge(base, nxt):
        return self.value_strategy("", base, nxt)

    def value_strategy(self, base, nxt):
        pass

    @staticmethod
    def _expand_strategies(strategy_list, strategy_dict):
        """
        given a list strategy_list,
        match the



always_merger = Merger()
always_exception = Merger()
