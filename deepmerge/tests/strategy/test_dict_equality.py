from copy import deepcopy
from typing import Any

import pytest

from deepmerge import Merger


@pytest.fixture
def merger():
    return Merger([(list, ["append_unique"])], ["override"], ["override"])


@pytest.mark.parametrize(
    "first,second",
    [
        ({"nested": {"x": 1, "y": 2}}, {"nested": {"y": 2, "x": 1}}),
        ({"value": 1}, {"value": 1.0}),
        ({"value": True}, {"value": 1}),
        ({1: "value"}, {1.0: "value"}),
        ({"value": {1, 2}}, {"value": frozenset({1, 2})}),
        ({"value": [{"x": 1}]}, {"value": [{"x": 1.0}]}),
        ({"value": ({1, 2},)}, {"value": (frozenset({1, 2}),)}),
        ({"value": b"a"}, {"value": bytearray(b"a")}),
        ({"value": range(3)}, {"value": range(0, 3)}),
        ({"value": b"a"}, {"value": memoryview(b"a")}),
    ],
)
@pytest.mark.parametrize("in_base", [False, True])
def test_equal_dictionary_values(merger, first, second, in_base):
    base = [first] if in_base else []
    incoming = [second] if in_base else [first, second]
    assert first == second
    before_base, before_incoming = base[:], incoming[:]
    result = merger.merge(base, incoming)
    assert result == [first]
    assert result[0] is first
    assert base == before_base
    assert incoming == before_incoming


def test_distinct_values_with_same_keys(merger):
    first, second = {"value": [1]}, {"value": [2]}
    assert merger.merge([first], [second]) == [first, second]


class EqualToOne:
    __hash__: Any = None

    def __eq__(self, other):
        return other == 1

    def __repr__(self):
        return "different representation"


@pytest.mark.parametrize("reverse", [False, True])
def test_custom_equality_fallback(merger, reverse):
    base, incoming = [{"value": 1}], [{"value": EqualToOne()}]
    if reverse:
        base, incoming = incoming, base
    assert merger.merge(base, incoming) == base


def test_recursive_values(merger):
    value = {}
    value["self"] = value
    assert merger.merge([value], []) == [value]


class AlwaysEqualDict(dict):
    def __eq__(self, other):
        return isinstance(other, dict)


@pytest.mark.parametrize("reverse", [False, True])
def test_dictionary_subclass_equality(merger, reverse):
    base, incoming = [AlwaysEqualDict(a=1)], [{"different": 2}]
    if reverse:
        base, incoming = incoming, base
    assert len(merger.merge(base, incoming)) == 1


def test_base_duplicates_and_distinct_containers(merger):
    first = {"value": [1]}
    different = {"value": (1,)}
    result = merger.merge([first, first], [deepcopy(first), different])
    assert result == [first, first, different]
    assert result[0] is first
    assert result[1] is first


def test_homogeneous_dictionary_index_is_not_quadratic(merger, monkeypatch):
    from deepmerge.extended_set import ExtendedSet

    candidate_count = 0
    original = ExtendedSet._hash_element

    def hash_element(self, element):
        nonlocal candidate_count
        result = original(self, element)
        candidate_count += len(self._buckets.get(result, []))
        return result

    monkeypatch.setattr(ExtendedSet, "_hash_element", hash_element)
    values = [{"value": {"number": i, "items": [i, i + 1]}} for i in range(1000)]
    result = merger.merge(values[:500], values[500:] + deepcopy(values))
    assert result == values
    # A key-set-only hash sends every dict to one bucket. Bound candidate
    # comparisons, not wall time, so this regression is machine-independent.
    assert candidate_count < 5000


def test_structural_hash_collisions_still_compare_values(merger, monkeypatch):
    from deepmerge.extended_set import ExtendedSet

    monkeypatch.setattr(ExtendedSet, "_hash_element", lambda self, value: 0)
    first, second = {"value": 1}, {"value": 2}
    assert merger.merge([first], [second, {"value": 1.0}]) == [first, second]
