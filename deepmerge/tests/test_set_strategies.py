"""Set strategies via a Merger, plus set-adjacent type behaviour.

Upstream tests call the set strategies only as bare static methods;
this file runs them through a Merger (including nested in dicts),
checks empty combinations and non-mutation, and pins down the
set/frozenset boundary, which is not a set merge at all.
"""

import pytest

from deepmerge import Merger, always_merger, merge_or_raise
from deepmerge.exception import InvalidMerge


def _set_merger(strategy):
    return Merger([(set, strategy)], ["override"], ["override"])


@pytest.mark.parametrize(
    "strategy,base,nxt,expected",
    [
        ("union", {1, 2}, {2, 3}, {1, 2, 3}),
        ("intersect", {1, 2}, {2, 3}, {2}),
        ("override", {1, 2}, {2, 3}, {2, 3}),
    ],
)
def test_set_strategies_basic(strategy, base, nxt, expected):
    assert _set_merger(strategy).merge(base, nxt) == expected


@pytest.mark.parametrize(
    "strategy,base,nxt,expected",
    [
        ("union", set(), {1}, {1}),
        ("union", {1}, set(), {1}),
        ("union", set(), set(), set()),
        ("intersect", set(), {1}, set()),
        ("intersect", {1}, set(), set()),
        ("override", set(), {1}, {1}),
        ("override", {1}, set(), set()),
    ],
)
def test_set_strategies_empty_combinations(strategy, base, nxt, expected):
    assert _set_merger(strategy).merge(base, nxt) == expected


@pytest.mark.parametrize("strategy", ["union", "intersect"])
def test_set_strategies_do_not_mutate_inputs(strategy):
    base = {1, 2}
    nxt = {2, 3}
    _set_merger(strategy).merge(base, nxt)
    assert base == {1, 2}
    assert nxt == {2, 3}


def test_set_union_returns_a_new_set():
    base = {1}
    result = _set_merger("union").merge(base, {2})
    assert result == {1, 2}
    assert result is not base


def test_set_override_returns_next_object():
    nxt = {2, 3}
    assert _set_merger("override").merge({1}, nxt) is nxt


def test_always_merger_unions_sets_nested_in_dicts():
    base = {"a": {1, 2}}
    assert always_merger.merge(base, {"a": {2, 3}}) == {"a": {1, 2, 3}}


def test_set_subclass_union_result_is_a_plain_set():
    class MySet(set):
        pass

    result = always_merger.merge(MySet([1]), MySet([2]))
    assert result == {1, 2}
    assert type(result) is set


def test_frozenset_is_not_merged_as_a_set():
    # frozenset is not an instance of set, so a set/frozenset pair is
    # a type conflict: always_merger takes the next value.
    assert always_merger.merge({1}, frozenset([2])) == frozenset([2])
    with pytest.raises(InvalidMerge) as exc_info:
        merge_or_raise.merge({1}, frozenset([2]))
    assert exc_info.value.strategy_list_name == "type conflict"


def test_frozenset_pair_uses_fallback_not_set_strategy():
    # Both sides frozenset: same-type fallback, so always_merger
    # overrides and merge_or_raise reports the fallback list.
    assert always_merger.merge(frozenset([1]), frozenset([2])) == frozenset([2])
    with pytest.raises(InvalidMerge) as exc_info:
        merge_or_raise.merge(frozenset([1]), frozenset([2]))
    assert exc_info.value.strategy_list_name == "fallback"
