"""ExtendedSet directly.

Upstream has no test file for ExtendedSet at all; it is only
exercised indirectly through append_unique. These tests pin down
its bucket-based membership for unhashable values, its hash-collision
handling, and two measured quirks: the underlying set storage is
never populated (so len() is 0 and iteration is empty), and set
operations therefore drop ExtendedSet elements.
"""

import pytest

from deepmerge.extended_set import ExtendedSet


def test_contains_hashable_values():
    es = ExtendedSet([1, 2, 3])
    assert 1 in es
    assert 2 in es
    assert 4 not in es


def test_contains_unhashable_dict_values():
    es = ExtendedSet([{"a": 1}])
    assert {"a": 1} in es
    assert {"a": 2} not in es


def test_dict_membership_ignores_key_order():
    es = ExtendedSet([{"a": 1, "b": 2}])
    assert {"b": 2, "a": 1} in es


def test_construction_deduplicates_equal_values():
    es = ExtendedSet([1, 1, 2, {"a": 1}, {"a": 1}])
    assert 1 in es
    assert 2 in es
    assert {"a": 1} in es
    assert {"a": 2} not in es


def test_contains_tuple_with_unhashable_member():
    es = ExtendedSet([([1],)])
    assert ([1],) in es
    assert ([2],) not in es


def test_contains_nested_unhashable_dict_value():
    es = ExtendedSet([{"a": [1]}])
    assert {"a": [1]} in es
    assert {"a": [2]} not in es


def test_hash_colliding_values_stay_distinct():
    # hash(-1) == hash(-2), but the two values are not equal.
    assert -1 not in ExtendedSet([-2])
    assert -2 not in ExtendedSet([-1])
    # Two dicts whose lossy "key:value" hash collides are kept apart.
    assert {"a": "1,b:2"} not in ExtendedSet([{"a": "1", "b": "2"}])
    assert {"k": "1"} not in ExtendedSet([{"k": 1}])


def test_empty_extended_set_contains_nothing():
    es = ExtendedSet([])
    assert 1 not in es
    assert {} not in es


def test_extended_set_is_a_set_subclass():
    assert isinstance(ExtendedSet([1]), set)


def test_len_and_iteration_do_not_reflect_buckets():
    # Measured quirk: __init__ only fills the private _buckets, never
    # the set storage, so len() is 0 and iteration yields nothing even
    # though membership tests work.
    es = ExtendedSet([1, 2, {"a": 1}])
    assert 1 in es
    assert len(es) == 0
    assert list(es) == []


def test_set_union_drops_extended_set_elements():
    # Measured consequence of the quirk above: set union reads the
    # (empty) set storage, not the buckets.
    es = ExtendedSet([1, 2])
    assert es | {3} == {3}
