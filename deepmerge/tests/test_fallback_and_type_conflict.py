"""Fallback and type-conflict strategies, and merge_or_raise errors.

Upstream covers ``override_if_not_empty`` as a bare static method and
one merge_or_raise case. This file covers the strategies through a
Merger (including ``override_if_not_empty`` as the type-conflict
strategy), the fallback/type-conflict distinction in InvalidMerge,
nested error paths, and the bool/int and custom-class corners.
"""

import pytest

from deepmerge import STRATEGY_END, Merger, always_merger, conservative_merger, merge_or_raise
from deepmerge.exception import InvalidMerge
from deepmerge.strategy.fallback import FallbackStrategies
from deepmerge.strategy.type_conflict import TypeConflictStrategies


def _scalar_merger(fallback, type_conflict):
    return Merger([(dict, "merge")], [fallback], [type_conflict])


@pytest.mark.parametrize(
    "base,nxt",
    [(1, 2), ("a", "b"), ((1,), (2,)), (None, None)],
)
def test_fallback_override_takes_next_for_same_type_scalars(base, nxt):
    assert _scalar_merger("override", "override").merge(base, nxt) == nxt


@pytest.mark.parametrize(
    "base,nxt",
    [(1, 2), ("a", "b"), ((1,), (2,)), (None, None)],
)
def test_fallback_use_existing_keeps_base_for_same_type_scalars(base, nxt):
    assert _scalar_merger("use_existing", "use_existing").merge(base, nxt) == base


def test_fallback_custom_callable_wins_over_later_strategies():
    merger = Merger(
        [(dict, "merge")],
        [lambda config, path, base, nxt: "FB", "override"],
        ["override"],
    )
    assert merger.merge(1, 2) == "FB"


def test_type_conflict_override_and_use_existing_via_dict_values():
    override = _scalar_merger("override", "override")
    assert override.merge({"a": 1}, {"a": "x"}) == {"a": "x"}
    keep = _scalar_merger("use_existing", "use_existing")
    assert keep.merge({"a": 1}, {"a": "x"}) == {"a": 1}


@pytest.mark.parametrize(
    "nxt,expected",
    [
        ("", 1),
        ([], 1),
        ({}, 1),
        (None, 1),
        ("x", "x"),
        (0, 0),
        (False, False),
        ([0], [0]),
    ],
)
def test_override_if_not_empty_as_type_conflict_strategy(nxt, expected):
    merger = Merger(
        [(dict, "merge")], ["override"], ["override_if_not_empty"]
    )
    assert merger.merge({"a": 1}, {"a": nxt}) == {"a": expected}


def test_fallback_statics_direct():
    assert FallbackStrategies.strategy_override(None, [], 1, 2) == 2
    assert FallbackStrategies.strategy_use_existing(None, [], 1, 2) == 1


def test_type_conflict_statics_direct():
    assert TypeConflictStrategies.strategy_override(None, [], 1, 2) == 2
    assert TypeConflictStrategies.strategy_use_existing(None, [], 1, 2) == 1


@pytest.mark.parametrize(
    "base,nxt",
    [(1, 2), ("a", "b"), ((1,), (2,))],
)
def test_merge_or_raise_same_type_scalars_fail_on_fallback(base, nxt):
    with pytest.raises(InvalidMerge) as exc_info:
        merge_or_raise.merge(base, nxt)
    assert exc_info.value.strategy_list_name == "fallback"
    assert exc_info.value.path == []
    assert exc_info.value.base == base
    assert exc_info.value.nxt == nxt


@pytest.mark.parametrize(
    "base,nxt",
    [(1, "x"), ({"a": 1}, [1]), ([1], {1}), (None, {"a": 1})],
)
def test_merge_or_raise_type_mismatches_fail_on_type_conflict(base, nxt):
    with pytest.raises(InvalidMerge) as exc_info:
        merge_or_raise.merge(base, nxt)
    assert exc_info.value.strategy_list_name == "type conflict"


def test_merge_or_raise_nested_paths_are_tracked():
    with pytest.raises(InvalidMerge) as exc_info:
        merge_or_raise.merge({"a": {"b": 1}}, {"a": {"b": "x"}})
    assert exc_info.value.strategy_list_name == "type conflict"
    assert exc_info.value.path == ["a", "b"]
    with pytest.raises(InvalidMerge) as exc_info:
        merge_or_raise.merge({"a": {"b": 1}}, {"a": {"b": 2}})
    assert exc_info.value.strategy_list_name == "fallback"
    assert exc_info.value.path == ["a", "b"]


def test_bool_and_int_are_not_a_type_conflict():
    # bool is a subclass of int, so an int/bool pair takes the
    # fallback path, not the type-conflict path.
    assert always_merger.merge(1, False) is False
    assert always_merger.merge(True, 2) == 2
    with pytest.raises(InvalidMerge) as exc_info:
        merge_or_raise.merge(1, False)
    assert exc_info.value.strategy_list_name == "fallback"


def test_custom_class_pairs_use_fallback_or_type_conflict():
    class A:
        pass

    class B(A):
        pass

    class C:
        pass

    a, b, c = A(), B(), C()
    # Same class, and either subclass direction, count as "similar
    # types" and take the fallback path.
    a2 = A()
    assert always_merger.merge(a, a2) is a2
    assert always_merger.merge(b, a) is a
    assert always_merger.merge(a, b) is b
    assert conservative_merger.merge(a, b) is a
    # Unrelated classes are a genuine type conflict.
    assert always_merger.merge(a, c) is c
    assert conservative_merger.merge(a, c) is a
    with pytest.raises(InvalidMerge) as exc_info:
        merge_or_raise.merge(a, c)
    assert exc_info.value.strategy_list_name == "type conflict"


def test_type_conflict_end_then_override_chain():
    merger = Merger(
        [(dict, "merge")],
        ["override"],
        [lambda config, path, base, nxt: STRATEGY_END, "override"],
    )
    assert merger.merge({"a": 1}, {"a": "x"}) == {"a": "x"}


def test_value_and_type_conflict_strategy_methods_direct():
    assert always_merger.value_strategy(["k"], 1, 2) == 2
    assert always_merger.type_conflict_strategy([], 1, "x") == "x"
    assert conservative_merger.type_conflict_strategy([], 1, "x") == 1
