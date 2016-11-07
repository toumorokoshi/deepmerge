def override(config, path, base, nxt):
    return nxt

TYPE_CONFLICT_STRATEGIES = {
    "override": override
}
