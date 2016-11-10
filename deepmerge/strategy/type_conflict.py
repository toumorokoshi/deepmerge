from .core import StrategyList


class TypeConflictStrategies(StrategyList):

    NAME = "type conflict"

    @staticmethod
    def strategy_override(config, path, base, nxt):
        return nxt
