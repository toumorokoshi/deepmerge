from .merger import Merger
from .strategy.core import STRATEGY_END

# some standard mergers available

# this merge will never raise an exception.
# in the case of type mismatches,
# the value from the second object
# will override the previous one.
always_merger = Merger(
    [
        (list, "append"),
        (dict, "merge")
    ],
    ["override"],
    ["override"]
)

# this merge strategies attempts
# to merge (append for list, unify for dicts)
# if possible, but raises an exception
# in the case of type conflicts.
merge_or_raise = Merger(
    [
        (list, "append"),
        (dict, "merge")
    ],
    [], []
)

# a conservative merge tactic:
# for data structures with a specific
# strategy, keep the existing value.
# similar to always_merger but instead
# keeps existing values when faced
# with a type conflict.
conservative_merger = Merger(
    [
        (list, "append"),
        (dict, "merge")
    ],
    ["use_existing"],
    ["use_existing"]
)
