from deepmerge import always_merger


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
