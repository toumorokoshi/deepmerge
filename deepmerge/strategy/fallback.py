from .core import StrategyList


class FallbackStrategies(StrategyList):

    NAME = "fallback"

    @staticmethod
    def strategy_override(config, path, base, nxt):
        return nxt
