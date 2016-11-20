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
