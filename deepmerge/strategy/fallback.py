from .core import StrategyList


class FallbackStrategies(StrategyList):
    """
    The StrategyList containing fallback strategies.
    """

    NAME = "fallback"

    @staticmethod
    def strategy_override(config, path, base, nxt):
        """ use nxt, and ignore base. """
        return nxt
