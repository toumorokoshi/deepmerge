class DeepMergeException(Exception):
    pass


class StrategyNotFound(DeepMergeException):
    pass


class InvalidMerge(DeepMergeException):
    pass
