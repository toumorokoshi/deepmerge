def override(config, path, base, nxt):
    return nxt


def prepend(config, path, base, nxt):
    return nxt + base


def append(config, path, base, nxt):
    return base + nxt

LIST_STRATEGIES = {
    "override": override,
    "prepend": prepend,
    "append": append
}
