import pytest
from deepmerge import (
    always_merger,
    conservative_merger,
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


@pytest.mark.parametrize("base, nxt, expected", [
    ("dooby", "fooby", "dooby"),
    (-10, "goo", -10)
])
def test_use_existing(base, nxt, expected):
    assert conservative_merger.merge(base, nxt) == expected

def test_example():
    base = {"foo": "value", "baz": ["a"]}
    next = {"bar": "value2", "baz": ["b"]}

    always_merger.merge(base, next)

    assert base == {
        "foo": "value",
        "bar": "value2",
        "baz": ["a", "b"]
    }

     