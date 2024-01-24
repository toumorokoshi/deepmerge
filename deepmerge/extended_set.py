from typing import Sequence, Any


class ExtendedSet(set):
    """
    ExtendedSet is an extension of set, which allows for usage
    of types that are typically not allowed in a set
    (e.g. unhashable).

    The following types that cannot be used in a set are supported:

    - unhashable types
    """

    def __init__(self, elements: Sequence) -> None:
        self._values_by_hash = {self._hash_element(e): e for e in elements}

    def _insert(self, element: Any) -> None:
        self._values_by_hash[self._hash_element(element)] = element
        return

    def _hash_element(self, element: Any) -> int:
        if getattr(element, "__hash__") is not None:
            return hash(element)
        return hash(str(element))

    def __contains__(self, obj: Any) -> bool:
        return self._hash_element(obj) in self._values_by_hash
