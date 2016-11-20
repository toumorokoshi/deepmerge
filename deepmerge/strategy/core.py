from ..exception import StrategyNotFound, InvalidMerge
from ..compat import string_type

STRATEGY_END = object()


class StrategyList(object):

    NAME = None

    def __init__(self, strategy_list):
        if not isinstance(strategy_list, list):
            strategy_list = [strategy_list]
        self._strategies = [
            self._expand_strategy(s) for s in strategy_list
        ]

    @classmethod
    def _expand_strategy(cls, strategy):
        """
        given a list strategy_list,
        match the appropriate strategy in the dict, or leave it
        if it is a function.
        """
        if isinstance(strategy, string_type):
            method_name = "strategy_{0}".format(strategy)
            if not hasattr(cls, method_name):
                raise StrategyNotFound(strategy)
            return getattr(cls, method_name)
        return strategy

    def __call__(self, *args, **kwargs):
        for s in self._strategies:
            ret_val = s(*args, **kwargs)
            if ret_val is not STRATEGY_END:
                return ret_val
        raise InvalidMerge("no more strategies found for {0} and arguments {1}, {2}".format(
            self.NAME, args, kwargs
        ))
