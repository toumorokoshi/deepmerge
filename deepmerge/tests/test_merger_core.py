"""Merger construction, StrategyList mechanics, and package presets.

Upstream tests a custom merger only lightly. This file covers
construction errors (StrategyNotFound / ValueError), callable
strategies for arbitrary types, strategy-list expansion rules, empty
strategy lists on every named subclass, and the preset mergers.
"""

import pytest

from deepmerge import (
    DEFAULT_TYPE_SPECIFIC_MERGE_STRATEGIES,
    Merger,
    always_merger,
    conservative_merger,
    merge_or_raise,
)
from deepmerge.exception import StrategyNotFound
from deepmerge.strategy.core import StrategyList
from deepmerge.strategy.dict import DictStrategies
from deepmerge.strategy.fallback import FallbackStrategies
from deepmerge.strategy.list import ListStrategies
from deepmerge.strategy.set import SetStrategies
from deepmerge.strategy.type_conflict import TypeConflictStrategies


def test_unknown_string_strategy_for_provided_type_raises():
    with pytest.raises(StrategyNotFound) as exc_info:
        Merger([(list, "bogus")], ["override"], ["override"])
    assert exc_info.value.args == ("bogus",)


def test_unknown_string_strategy_for_fallback_raises():
    with pytest.raises(StrategyNotFound):
        Merger([(dict, "merge")], ["bogus"], ["override"])


def test_unknown_string_strategy_for_type_conflict_raises():
    with pytest.raises(StrategyNotFound):
        Merger([(dict, "merge")], ["override"], ["bogus"])


def test_non_callable_strategy_for_unknown_type_raises_value_error():
    with pytest.raises(ValueError, match="Cannot handle"):
        Merger([(int, "override")], ["override"], ["override"])


def test_callable_strategy_for_unknown_type_works():
    merger = Merger(
        [(int, lambda config, path, base, nxt: base + nxt)],
        ["override"],
        ["override"],
    )
    assert merger.merge(1, 2) == 3


def test_object_strategy_catches_everything_when_listed_first():
    merger = Merger(
        [(object, lambda config, path, base, nxt: "OBJ")],
        ["override"],
        ["override"],
    )
    assert merger.merge(1, 2) == "OBJ"
    assert merger.merge({"a": 1}, {"b": 2}) == "OBJ"


def test_object_strategy_after_dict_only_catches_non_dicts():
    merger = Merger(
        [(dict, "merge"), (object, lambda config, path, base, nxt: "OBJ")],
        ["override"],
        ["override"],
    )
    assert merger.merge({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}
    assert merger.merge(1, 2) == "OBJ"


def test_strategy_list_accepts_a_single_string_not_just_a_list():
    assert FallbackStrategies("override")(None, [], 1, 9) == 9
    assert FallbackStrategies("use_existing")(None, [], 1, 9) == 1


def test_strategy_list_unknown_string_raises_on_construction():
    with pytest.raises(StrategyNotFound):
        StrategyList("bogus")


def test_strategy_list_first_non_end_strategy_wins():
    def end_fn(config, path, base, nxt):
        from deepmerge import STRATEGY_END

        return STRATEGY_END

    sl = StrategyList([end_fn, lambda config, path, base, nxt: 42])
    assert sl(None, [], 1, 2) == 42


@pytest.mark.parametrize(
    "cls,name",
    [
        (FallbackStrategies, "fallback"),
        (TypeConflictStrategies, "type conflict"),
        (DictStrategies, "dict"),
        (ListStrategies, "list"),
        (SetStrategies, "set"),
    ],
)
def test_empty_strategy_list_on_named_subclass_raises_invalid_merge(cls, name):
    from deepmerge.exception import InvalidMerge

    with pytest.raises(InvalidMerge) as exc_info:
        cls([])(None, [], 1, 2)
    assert exc_info.value.strategy_list_name == name


def test_merge_return_shape_by_top_level_type():
    base = {"a": 1}
    assert always_merger.merge(base, {"b": 2}) is base
    assert always_merger.merge([1], [2]) == [1, 2]
    assert always_merger.merge(5, 9) == 9
    assert conservative_merger.merge(5, 9) == 5


def test_sequential_merges_accumulate():
    data = {"a": [1]}
    always_merger.merge(data, {"a": [2]})
    always_merger.merge(data, {"a": [3]})
    assert data == {"a": [1, 2, 3]}


def test_default_type_specific_strategies_content():
    assert DEFAULT_TYPE_SPECIFIC_MERGE_STRATEGIES == [
        (list, "append"),
        (dict, "merge"),
        (set, "union"),
    ]


def test_presets_are_distinct_merger_instances():
    assert isinstance(always_merger, Merger)
    assert isinstance(conservative_merger, Merger)
    assert isinstance(merge_or_raise, Merger)
    assert always_merger is not conservative_merger
    assert always_merger is not merge_or_raise
