User Guide
----------

Simple Usage
============

deepmerge was written as a library to help construct merge functions, eliminating some of the boilerplate around recursing
through common data structures and joining results. Although
it's recommended to choose your own strategies, deepmerge does
provided some preconfigured mergers for a common situations:

* deepmerge.always_merger: always try to merge. in the case of mismatches, the value from the second object overrides the first one.
* deepmerge.merge_or_raise: try to merge, raise an exception if an unmergable situation is encountered.
* deepmerge.conservative_merger: similar to always_merger, but in the case of a conflict, use the existing value.

Once a merger is constructed, it then has a merge() method that can be called:

.. code-block:: python

    from deepmerge import always_merger

    base = {"foo": "value", "baz": ["a"]}
    next = {"bar": "value2", "baz": ["b"]}

    always_merger.merge(base, next)

    assert base == {
        "foo": "value",
        "bar": "value2",
        "baz": ["a", "b"]
    }

Merges are Destructive
======================

You may have noticed from the example, but merging is a destructive behavior: it will modify the first argument passed in (the base) as part of the merge.

This is intentional, as an implicit copy would result in a significant performance slowdown for deep data structures. If you need to keep the original objects unmodified, you can use the deepcopy method:

.. code-block:: python

    from copy import deepcopy
    result = deepcopy(base)
    always_merger.merge(result, next)

    assert id(result) != id(base)

Authoring your own Mergers
==========================

The :class:`deepmerge.merger.Merger` class enacts the merging strategy,
and stores the configuration about the merging strategy chosen.

The merger takes a list of a combination of strings or functions,
which are expanded into strategies that are attempted in the order in
the list.

For example, a list of ["append", "merge"] will attempt the "append"
strategy first, and attempt the merge strategy if append is not able
to merge the structures.

If none of the strategies were able to merge the structures (or if non
exists), a :py:exc:`deepmerge.exception.InvalidMerge` exception is raised.

----------
Strategies
----------

The merger class alone does not make any decisions around merging the
code. This is instead deferred to the strategies themselves.

Built-in Strategies
===================

If you name a strategy with a string, it will attempt to match that with
the merge strategies that are built into deepmerge. You can see a list
of which strategies exist for which types at :doc:`./strategies`

Custom Strategies
=================

Strategies are functions that satisfy the following properties:

* have the function signature (config, path, base, nxt)
* return the merged object, or `deepmerge.STRATEGY_END`.

Example:

.. code-block:: python

   def append_last_element(config, path, base, nxt):
       """ a list strategy to append the last element of nxt only. """
       if len(nxt) > 0:
          base.append(nxt[-1])
          return base

If a strategy fails, an exception should not be raised, instead it should return `deepmerge.STRATEGY_END`. This is to
ensure it can be chained with other strategies, or the fall-back.

Uniqueness of elements when merging
===================================

Some strategies require determining the uniqueness
of the elements. Since deepmerge primarily deals with nested
types, this includes structures that are not hashable such as
dictionaries.

In those cases, built-in deepmerge strategies will call repr()
on the object and hash that value instead.
