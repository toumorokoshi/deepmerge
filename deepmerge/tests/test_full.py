import pytest
from deepmerge import (
    always_merger,
    merge_or_raise,
)


def test_fill_missing_value():
    base = {
        "foo": 0,
        "baz": 2
    }
    nxt = {
        "bar": 1
    }
    always_merger.merge(base, nxt)
    assert base == {
        "foo": 0, "bar": 1, "baz": 2
    }


def test_merge_or_raise_raises_exception():
    base = {
        "foo": 0,
        "baz": 2
    }
    nxt = {
        "bar": 1,
        "foo": "a string!"
    }
    with pytest.raises(Exception):
        merge_or_raise.merge(base, nxt)
