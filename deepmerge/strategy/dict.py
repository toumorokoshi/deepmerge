def merge(config, path, base, nxt):
    for k, v in nxt.items():
        if k not in base:
            base[k] = v
        else:
            new_path = path + "." + k
            base[k] = config.value_strategy(new_path, base[k], v)
    return base


def override(config, path, base, nxt):
    return nxt


DICT_STRATEGIES = {
    "merge": merge,
    "override": override
}
