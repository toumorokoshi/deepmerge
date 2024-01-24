from __future__ import annotations

from typing import Dict, List

import deepmerge.merger
from .core import StrategyList


class DictStrategies(StrategyList):
    """
    Contains the strategies provided for dictionaries.

    """

    NAME = "dict"

    @staticmethod
    def strategy_merge(
        config: deepmerge.merger.Merger, path: List, base: Dict, nxt: Dict
    ) -> Dict:
        """
        for keys that do not exists,
        use them directly. if the key exists
        in both dictionaries, attempt a value merge.
        """
        for k, v in nxt.items():
            if k not in base:
                base[k] = v
            else:
                base[k] = config.value_strategy(path + [k], base[k], v)
        return base

    @staticmethod
    def strategy_override(
        config: deepmerge.merger.Merger, path: List, base: Dict, nxt: Dict
    ) -> Dict:
        """
        move all keys in nxt into base, overriding
        conflicts.
        """
        return nxt
