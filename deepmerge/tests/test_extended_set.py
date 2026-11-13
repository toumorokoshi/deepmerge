import pytest

from deepmerge.extended_set import ExtendedSet


def test_len_counts_inserted_elements():
    es = ExtendedSet([1, 2, 3])
    assert len(es) == 3


def test_iteration_yields_inserted_elements():
    es = ExtendedSet([1, 2, 3])
    assert sorted(es) == [1, 2, 3]


def test_truthiness_reflects_contents():
    assert bool(ExtendedSet([1]))
    assert not bool(ExtendedSet([]))


def test_equality_compares_contents():
    assert ExtendedSet([1, 2]) == ExtendedSet([1, 2])
    assert ExtendedSet([1, 2]) != ExtendedSet([1, 3])


def test_not_equal_to_empty_set_when_nonempty():
    # A nonempty ExtendedSet used to compare equal to set() because
    # the inherited set.__eq__ only saw the (never-initialized)
    # underlying set storage.
    assert ExtendedSet([1, 2]) != set()
    assert set() != ExtendedSet([1, 2])


def test_membership_still_works():
    es = ExtendedSet([1, 2, 3])
    assert 1 in es
    assert 4 not in es


def test_membership_with_unhashable_elements():
    es = ExtendedSet([{"a": 1}, ([1],), [1, 2]])
    assert {"a": 1} in es
    assert ([1],) in es
    assert [1, 2] in es
    assert {"a": 2} not in es


def test_repr_shows_contents():
    es = ExtendedSet([1, 2, 3])
    assert "1" in repr(es)
