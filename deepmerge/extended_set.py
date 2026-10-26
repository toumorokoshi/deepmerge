from typing import Sequence, Any, Dict, List, Optional, Set


class ExtendedSet(set):
    """
    A membership index for hashable and unhashable values.

    Built-in containers are indexed by equality-compatible structural hashes.
    Custom objects and recursive containers use equality scans instead, since
    their equality cannot safely be inferred from their representation.
    Values must not change while they are in the index.
    """

    def __init__(self, elements: Sequence) -> None:
        self._buckets: Dict[int, List[Any]] = {}
        self._fallback: List[Any] = []
        self._elements: List[Any] = []
        for element in elements:
            self._insert(element)

    def _insert(self, element: Any) -> None:
        key = self._hash_element(element)
        candidates = self._candidates(key)
        if not any(element == existing for existing in candidates):
            if key is None:
                self._fallback.append(element)
            else:
                self._buckets.setdefault(key, []).append(element)
            self._elements.append(element)

    def _hash_element(self, element: Any) -> Optional[int]:
        return self._structural_hash(element, set())

    def _structural_hash(self, element: Any, active: Set[int]) -> Optional[int]:
        # Exact types only: subclasses can define different equality rules.
        kind = type(element)
        if kind in (type(None), bool, int, float, complex, str, bytes):
            return hash(element)
        if kind is bytearray:
            return hash(bytes(element))
        if kind not in (dict, list, tuple, set, frozenset):
            return None
        identity = id(element)
        if identity in active:
            return None
        active.add(identity)
        try:
            if kind is dict:
                pairs = []
                for key, value in element.items():
                    key_hash = self._structural_hash(key, active)
                    value_hash = self._structural_hash(value, active)
                    if key_hash is None or value_hash is None:
                        return None
                    pairs.append((key_hash, value_hash))
                return hash(("dict", frozenset(pairs)))
            hashes = []
            for value in element:
                value_hash = self._structural_hash(value, active)
                if value_hash is None:
                    return None
                hashes.append(value_hash)
            if kind in (set, frozenset):
                return hash(("set", frozenset(hashes)))
            return hash((kind, tuple(hashes)))
        finally:
            active.remove(identity)

    def _candidates(self, key: Optional[int]) -> List[Any]:
        if key is None:
            return self._elements
        return self._buckets.get(key, []) + self._fallback

    def __contains__(self, obj: Any) -> bool:
        return any(obj == existing for existing in self._candidates(self._hash_element(obj)))
