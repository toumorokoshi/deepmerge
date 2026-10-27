"""Preset mergers compared side by side.

Upstream tests each preset in isolation on a few flat cases. This
file runs the same inputs through always_merger, conservative_merger
and merge_or_raise, including matching-type merges that merge_or_raise
handles fine and conflict cases where it must raise.
"""

import pytest

from deepmerge import always_merger, conservative_merger, merge_or_raise
from deepmerge.exception import InvalidMerge


def test_merge_or_raise_merges_matching_types_exactly():
    assert merge_or_raise.merge([1, 2], [3]) == [1, 2, 3]
    assert merge_or_raise.merge({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}
    assert merge_or_raise.merge({1}, {2}) == {1, 2}
    assert merge_or_raise.merge({"a": {"x": 1}}, {"a": {"y": 2}}) == {
        "a": {"x": 1, "y": 2}
    }


@pytest.mark.parametrize(
    "base,nxt,always_expected,conservative_expected",
    [
        (1, "x", "x", 1),
        ({"a": 1}, [1], [1], {"a": 1}),
        (None, {"a": 1}, {"a": 1}, None),
        ({"a": None}, {"a": 5}, {"a": 5}, {"a": None}),
    ],
)
def test_preset_matrix_on_type_conflicts(
    base, nxt, always_expected, conservative_expected
):
    # Each merger gets a fresh copy: dict merges mutate base in
    # place, so reusing one base across mergers would contaminate
    # the later assertions.
    import copy

    assert always_merger.merge(copy.deepcopy(base), copy.deepcopy(nxt)) == always_expected
    assert (
        conservative_merger.merge(copy.deepcopy(base), copy.deepcopy(nxt))
        == conservative_expected
    )
    with pytest.raises(InvalidMerge):
        merge_or_raise.merge(copy.deepcopy(base), copy.deepcopy(nxt))


def test_presets_agree_on_matching_dict_merge():
    nxt = {"a": {"y": 2}, "lst": [2], "s": {2}}
    assert always_merger.merge(
        {"a": {"x": 1}, "lst": [1], "s": {1}}, nxt
    ) == {"a": {"x": 1, "y": 2}, "lst": [1, 2], "s": {1, 2}}
    assert conservative_merger.merge(
        {"a": {"x": 1}, "lst": [1], "s": {1}}, nxt
    ) == {"a": {"x": 1, "y": 2}, "lst": [1, 2], "s": {1, 2}}


def test_merge_or_raise_none_pair_fails_on_fallback():
    # None/None is a same-type pair, so it takes the (empty) fallback
    # list, not the type-conflict list.
    with pytest.raises(InvalidMerge) as exc_info:
        merge_or_raise.merge(None, None)
    assert exc_info.value.strategy_list_name == "fallback"
    assert exc_info.value.path == []


def test_always_never_raises_on_type_conflicts():
    assert always_merger.merge(1, "x") == "x"
    assert always_merger.merge({"a": 1}, [1]) == [1]
    assert always_merger.merge([1], {"a": 1}) == {"a": 1}
    assert always_merger.merge(None, {"a": 1}) == {"a": 1}


def test_conservative_always_keeps_existing_on_type_conflicts():
    assert conservative_merger.merge(1, "x") == 1
    assert conservative_merger.merge({"a": 1}, [1]) == {"a": 1}
    assert conservative_merger.merge([1], {"a": 1}) == [1]
    assert conservative_merger.merge(None, {"a": 1}) is None
