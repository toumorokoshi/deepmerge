import copy
from .strategy.value import VALUE_STRATEGIES
from .strategy.list import LIST_STRATEGIES
from .strategy.dict import DICT_STRATEGIES
from .strategy.type_conflict import TYPE_CONFLICT_STRATEGIES


def deep_merge(base, nxt):
    """
    performs a destructive merge of values in nxt into base.
    """

    props =


def _deep_merge(config, base, next_values):
    for k, v in next_values:
        if k not in base:
            base[k] = v
        else:
            base[k] = config.value_strategy(config, base[k], v)


def value_strategy(config, lhs, rhs):


class MergeProps(object):

    VALUE_STRATEGIES = set(["override", "merge"])
    TYPE_CONFLICT_STRATEGY = set(["override"])
    DICT_STRATEGY = set(["merge", "override"])
    LIST_STRATEGIES = set(["prepend", "append", "override"])

    def __init__(self):
        self.copy = False
        self.list_strategy = True
        self.override = False
        pass
