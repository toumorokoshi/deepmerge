from .merger import Merger

# some standard mergers available

always_merger = Merger(
    ["merge"],
    ["append"],
    ["merge"],
    ["override"]
)
