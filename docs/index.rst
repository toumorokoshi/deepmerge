.. deepmerge documentation master file, created by
   sphinx-quickstart on Sun Nov 20 11:31:44 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Deepmerge: merging nested data structures
=========================================

Deepmerge is a flexible library to handle merging of
nested data structures in Python (e.g. lists, dicts).

-------
Example
-------

.. code-block:: python

    from deepmerge import Merger

    my_merger = Merger(
        # pass in a list of tuple, with the
        # strategies you are looking to apply
        # to each type.
        [
            (list, ["append"]),
            (dict, ["merge"])
        ],
        # next, choose the fallback strategies,
        # applied to all other types:
        ["override"],
        # finally, choose the strategies in
        # the case where the types conflict:
        ["override"]
    )
    base = {"foo": ["bar"]}
    next = {"bar": "baz"}
    my_merger.merge(base, next)
    assert base == {"foo": ["bar"], "bar": "baz"}

----------------
The Merger Class
----------------

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
of which strategies exist for which types in the API docs.

Custom Strategies
=================

Strategies are functions that satisfy the following properties:

* have the function signature (config, path, base, nxt)
* return the merged object, or None.

Example:

.. code-block:: python

   def append_last_element(config, path, base, nxt):
       """ a list strategy to append the last element of nxt only. """
       if len(nxt) > 0:
          base.append(nxt[-1])
          return base

If a strategy fails, an exception should not be raised. This is to
ensure it can be chained with other strategies, or the fall-back.

----------------
Provided Mergers
----------------

Merge strategies vary wildly depending on the purpose, and thus it's
recommended to construct your own.

However, a few mergers are provided as a convenience. these are:




Contents:

.. toctree::
   :maxdepth: 2

   index
   strategies
   api



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
