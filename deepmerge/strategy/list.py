from .core import StrategyList


class ListStrategies(StrategyList):

    NAME = "list"

    @staticmethod
    def strategy_override(config, path, base, nxt):
        return nxt

    @staticmethod
    def strategy_prepend(config, path, base, nxt):
        return nxt + base

    @staticmethod
    def strategy_append(config, path, base, nxt):
        return base + nxt
