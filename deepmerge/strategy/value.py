from .core import STRATEGY_END


def override(merger, path, base, nxt):
    return nxt


def merge(merger, path, base, nxt):
    if not isinstance(base, nxt) or isinstance(nxt, base):
        return merger.type_conflict(path, base, nxt)
    if isinstance(base, dict):
        return merger.dict_strategy(path, base, nxt)
    if isinstance(base, list):
        return merger.list_strategy(path, base, nxt)
    return STRATEGY_END


VALUE_STRATEGIES = {
    "override": override,
    "merge": merge
}
