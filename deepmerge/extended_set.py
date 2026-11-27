from typing import Sequence, Any, Dict, List


class ExtendedSet(set):
    """
    ExtendedSet is an extension of set, which allows for usage
    of types that are typically not allowed in a set
    (e.g. unhashable).

    The following types that cannot be used in a set are supported:

    - unhashable types, granted they are idempotent, including tuples
      containing unhashable values.
    """

    def __init__(self, elements: Sequence) -> None:
        # Elements are grouped into buckets keyed by their (possibly lossy)
        # hash. Membership and insertion compare a candidate against the
        # members of the matching bucket using equality, so two distinct
        # elements that merely collide on the hash are not treated as equal.
        self._buckets: Dict[int, List[Any]] = {}
        for element in elements:
            self._insert(element)

    def _insert(self, element: Any) -> None:
        bucket = self._buckets.setdefault(self._hash_element(element), [])
        if not any(element == existing for existing in bucket):
            bucket.append(element)
        return

    def _hash_element(self, element: Any) -> int:
        try:
            return hash(element)
        except TypeError:
            # Defining __hash__ does not guarantee that hashing succeeds:
            # tuples may contain unhashable members.
            pass

        if isinstance(element, dict):
            sorted_keys = sorted(element.keys(), key=repr)
            return hash(",".join([f"{key}:{element[key]}" for key in sorted_keys]))
        else:
            return hash(str(element))

    def __contains__(self, obj: Any) -> bool:
        bucket = self._buckets.get(self._hash_element(obj))
        if bucket is None:
            return False
        return any(obj == existing for existing in bucket)

    def __iter__(self) -> Any:
        for bucket in self._buckets.values():
            yield from bucket

    def __len__(self) -> int:
        return sum(len(bucket) for bucket in self._buckets.values())

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ExtendedSet):
            return len(self) == len(other) and all(x in other for x in self)
        if isinstance(other, (set, frozenset)):
            # A real set can only contain hashable values, so an
            # ExtendedSet holding unhashable values can never equal one.
            # Note: set(...) cannot take self directly, as the constructor
            # copies the underlying set storage instead of iterating self.
            try:
                return set(list(self)) == other
            except TypeError:
                return False
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __repr__(self) -> str:
        return f"{type(self).__name__}({list(self)!r})"
