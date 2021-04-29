from .core import StrategyList


class ListStrategies(StrategyList):
    """
    Contains the strategies provided for lists.
    """

    NAME = "list"

    @staticmethod
    def strategy_override(config, path, base, nxt):
        """ use the list nxt. """
        return nxt

    @staticmethod
    def strategy_prepend(config, path, base, nxt):
        """ prepend nxt to base. """
        return nxt + base

    @staticmethod
    def strategy_append(config, path, base, nxt):
        """ append nxt to base. """
        return base + nxt

    @staticmethod
    def strategy_append_unduplicated(config, path, base, nxt):
        """ append unduplicated items in nxt to base. """
        return base + [n for n in nxt if n not in base]
