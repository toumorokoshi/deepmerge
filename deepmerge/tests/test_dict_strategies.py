"""Dict strategies: merge / override, mutation semantics, nesting.

Existing upstream tests only exercise dict merge indirectly through
``always_merger`` on flat dicts, so everything here targets the gaps:
in-place mutation, identity of nested / new values, deep nesting,
list values inside dicts, and first-entry-wins ordering.
"""

import pytest

from deepmerge import Merger, always_merger, conservative_merger
from deepmerge.strategy.dict import DictStrategies


def _merge_merger():
    return Merger([(dict, "merge")], ["override"], ["override"])


def _override_merger():
    return Merger([(dict, "override")], ["override"], ["override"])


def test_merge_disjoint_keys_returns_base_and_mutates_it():
    base = {"a": 1}
    result = _merge_merger().merge(base, {"b": 2})
    assert result is base
    assert base == {"a": 1, "b": 2}


def test_merge_preserves_base_only_keys():
    base = {"keep": 1, "shared": 1}
    result = _merge_merger().merge(base, {"shared": 2, "new": 3})
    assert result == {"keep": 1, "shared": 2, "new": 3}


def test_merge_overlapping_scalar_always_takes_next():
    base = {"a": 1}
    assert always_merger.merge(base, {"a": 2}) == {"a": 2}


def test_merge_overlapping_scalar_conservative_keeps_base():
    base = {"a": 1}
    assert conservative_merger.merge(base, {"a": 2}) == {"a": 1}


def test_merge_three_levels_deep():
    base = {"a": {"b": {"c": 1, "keep": 0}}}
    result = _merge_merger().merge(base, {"a": {"b": {"c": 2, "d": 3}}})
    assert result == {"a": {"b": {"c": 2, "keep": 0, "d": 3}}}


def test_merge_mutates_nested_dict_in_place():
    inner = {"x": 1}
    base = {"a": inner}
    result = _merge_merger().merge(base, {"a": {"y": 2}})
    assert result["a"] is inner
    assert inner == {"x": 1, "y": 2}


def test_merge_replaces_nested_list_without_mutating_original():
    # always_merger is used here because a dict-only merger has no
    # list strategy: a nested list pair would take the fallback path
    # (override) instead of appending.
    original_list = [1]
    base = {"lst": original_list}
    result = always_merger.merge(base, {"lst": [2]})
    assert result["lst"] == [1, 2]
    assert original_list == [1]
    assert result["lst"] is not original_list


def test_merge_new_key_value_is_same_object_not_a_copy():
    value = [1, 2]
    base = {}
    _merge_merger().merge(base, {"k": value})
    assert base["k"] is value


def test_merge_list_values_append_instead_of_merging_elements():
    # Lists inside dicts are appended wholesale; their dict elements
    # are NOT merged with each other.
    base = {"k": [{"a": 1}]}
    result = always_merger.merge(base, {"k": [{"a": 2}]})
    assert result == {"k": [{"a": 1}, {"a": 2}]}


@pytest.mark.parametrize(
    "base,nxt,expected",
    [
        ({}, {"a": 1}, {"a": 1}),
        ({"a": 1}, {}, {"a": 1}),
        ({}, {}, {}),
        ({"a": {"x": 1}}, {}, {"a": {"x": 1}}),
    ],
)
def test_merge_empty_dict_combinations(base, nxt, expected):
    assert _merge_merger().merge(base, nxt) == expected


def test_dict_override_returns_next_object_unchanged_base():
    base = {"a": 1, "x": 9}
    nxt = {"b": 2}
    result = _override_merger().merge(base, nxt)
    assert result is nxt
    assert base == {"a": 1, "x": 9}


def test_dict_override_inside_nested_merge():
    # A dict-override merger applied to a nested value replaces the
    # whole nested dict instead of merging it.
    merger = Merger([(dict, "override")], ["override"], ["override"])
    assert merger.merge({"a": {"x": 1}}, {"a": {"y": 2}}) == {"a": {"y": 2}}


def test_first_dict_entry_wins_over_later_ones():
    merge_first = Merger(
        [(dict, "merge"), (dict, "override")], ["override"], ["override"]
    )
    assert merge_first.merge({"a": 1, "x": 9}, {"a": 2}) == {"a": 2, "x": 9}
    override_first = Merger(
        [(dict, "override"), (dict, "merge")], ["override"], ["override"]
    )
    assert override_first.merge({"a": 1, "x": 9}, {"a": 2}) == {"a": 2}


def test_dict_value_replaced_by_scalar_and_vice_versa():
    assert always_merger.merge({"a": {"x": 1}}, {"a": 5}) == {"a": 5}
    assert always_merger.merge({"a": 5}, {"a": {"x": 1}}) == {"a": {"x": 1}}
    assert conservative_merger.merge({"a": {"x": 1}}, {"a": 5}) == {"a": {"x": 1}}


def test_strategy_merge_static_disjoint_keys_needs_no_config():
    # With no overlapping key, value_strategy is never called, so the
    # config argument is never used.
    base = {"a": 1}
    result = DictStrategies.strategy_merge(None, [], base, {"b": 2})
    assert result is base
    assert base == {"a": 1, "b": 2}


def test_merge_set_values_inside_dict_use_union():
    base = {"s": {1}}
    assert always_merger.merge(base, {"s": {2}}) == {"s": {1, 2}}
