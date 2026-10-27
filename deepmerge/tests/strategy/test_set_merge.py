from deepmerge.strategy.set import SetStrategies


def test_union_unions():
    assert SetStrategies.strategy_union({}, [], set("abc"), set("bcd")) == set("abcd")


def test_intersect_intersects():
    assert SetStrategies.strategy_intersect({}, [], set("abc"), set("bcd")) == set("bc")


def test_override_overrides():
    assert SetStrategies.strategy_override({}, [], set("abc"), set("bcd")) == set("bcd")


import pytest

from deepmerge import always_merger, merge_or_raise
from deepmerge.exception import InvalidMerge


def test_frozenset_is_not_merged_as_a_set():
    assert always_merger.merge({1}, frozenset([2])) == frozenset([2])
    with pytest.raises(InvalidMerge) as exc_info:
        merge_or_raise.merge({1}, frozenset([2]))
    assert exc_info.value.strategy_list_name == "type conflict"
