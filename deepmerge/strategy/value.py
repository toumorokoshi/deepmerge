from .core import STRATEGY_END, StrategyList


class ValueStrategies(StrategyList):

    NAME = "value"

    @staticmethod
    def strategy_override(merger, path, base, nxt):
        return nxt

    @staticmethod
    def strategy_merge(merger, path, base, nxt):
        if not (isinstance(base, type(nxt)) or isinstance(nxt, type(base))):
            return merger.type_conflict_strategy(path, base, nxt)
        if isinstance(base, dict):
            return merger.dict_strategy(path, base, nxt)
        if isinstance(base, list):
            return merger.list_strategy(path, base, nxt)
        return STRATEGY_END
