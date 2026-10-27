"""List strategies: append / prepend / override via a Merger.

Upstream tests cover ``append_unique`` almost exclusively, so this
file covers the three other strategies, their empty combinations,
their non-mutating behaviour, and strategy-chain (STRATEGY_END)
fall-through inside a Merger.
"""

import pytest

from deepmerge import STRATEGY_END, Merger, always_merger


def _list_merger(strategy):
    return Merger([(list, strategy)], ["override"], ["override"])


@pytest.mark.parametrize(
    "strategy,base,nxt,expected",
    [
        ("append", [1, 2], [3], [1, 2, 3]),
        ("prepend", [1, 2], [3], [3, 1, 2]),
        ("override", [1, 2], [3], [3]),
    ],
)
def test_list_strategies_basic(strategy, base, nxt, expected):
    assert _list_merger(strategy).merge(base, nxt) == expected


@pytest.mark.parametrize(
    "strategy,base,nxt,expected",
    [
        ("append", [], [1], [1]),
        ("append", [1], [], [1]),
        ("append", [], [], []),
        ("prepend", [], [1], [1]),
        ("prepend", [1], [], [1]),
        ("prepend", [], [], []),
        ("override", [], [1], [1]),
        ("override", [1], [], []),
    ],
)
def test_list_strategies_empty_combinations(strategy, base, nxt, expected):
    assert _list_merger(strategy).merge(base, nxt) == expected


@pytest.mark.parametrize("strategy", ["append", "prepend"])
def test_append_and_prepend_do_not_mutate_inputs(strategy):
    base = [1, 2]
    nxt = [3]
    _list_merger(strategy).merge(base, nxt)
    assert base == [1, 2]
    assert nxt == [3]


def test_append_returns_a_new_list_not_base():
    base = [1, 2]
    result = _list_merger("append").merge(base, [3])
    assert result == [1, 2, 3]
    assert result is not base


def test_list_override_returns_next_object():
    nxt = [3]
    assert _list_merger("override").merge([1, 2], nxt) is nxt


def test_always_merger_appends_top_level_lists():
    assert always_merger.merge([1], [2]) == [1, 2]


def test_always_merger_appends_lists_nested_in_dicts():
    base = {"foo": ["bar"]}
    assert always_merger.merge(base, {"foo": ["baz"]}) == {"foo": ["bar", "baz"]}


def test_strategy_chain_falls_through_on_strategy_end():
    def end_if_short(config, path, base, nxt):
        if len(base) < 2:
            return STRATEGY_END
        return "big"

    merger = Merger(
        [(list, [end_if_short, "append"])], ["override"], ["override"]
    )
    assert merger.merge([1], [9]) == [1, 9]
    assert merger.merge([1, 2], [9]) == "big"


def test_custom_list_callable_replaces_string_strategy():
    merger = Merger(
        [(list, lambda config, path, base, nxt: ["X"])],
        ["override"],
        ["override"],
    )
    assert merger.merge([1], [2]) == ["X"]


def test_append_unique_empty_combinations():
    # append_unique itself is covered upstream; only the empty
    # combinations (not covered there) are asserted here.
    merger = _list_merger("append_unique")
    assert merger.merge([], [1, 1, 2]) == [1, 2]
    assert merger.merge([1], []) == [1]
    assert merger.merge([], []) == []


def test_list_strategy_applies_only_when_both_sides_are_lists():
    # A list on one side and a scalar on the other is a type
    # conflict, not a list merge, even for always_merger.
    assert always_merger.merge([1], "x") == "x"
    assert always_merger.merge({"k": [1]}, {"k": "x"}) == {"k": "x"}
