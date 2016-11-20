from deepmerge.strategy.core import StrategyList


def test_single_value_allowed():
    """ """
    def strat(name):
        return name

    sl = StrategyList(strat)
    assert sl("foo") == "foo"
