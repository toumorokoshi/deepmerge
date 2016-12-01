from .core import StrategyList


class TypeConflictStrategies(StrategyList):
    """ contains the strategies provided for type conflicts. """

    NAME = "type conflict"

    @staticmethod
    def strategy_override(config, path, base, nxt):
        """ overrides the new object over the old object """
        return nxt
