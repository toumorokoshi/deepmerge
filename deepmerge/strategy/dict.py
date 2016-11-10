from .core import StrategyList


class DictStrategies(StrategyList):

    NAME = "dict"

    @staticmethod
    def strategy_merge(config, path, base, nxt):
        for k, v in nxt.items():
            if k not in base:
                base[k] = v
            else:
                base[k] = config.value_strategy(path + [k], base[k], v)
        return base

    @staticmethod
    def strategy_override(config, path, base, nxt):
        return nxt
