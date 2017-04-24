from .merger import Merger

# some standard mergers available

always_merger = Merger(
    [
        (list, "append"),
        (dict, "merge")
    ],
    ["override"],
    ["override"]
)

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
conservative_merger = Merger(
    [
        (list, "append"),
        (dict, "merge")
    ],
    ["use_existing"],
    ["use_existing"]
)
