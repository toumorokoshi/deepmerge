=========
deepmerge
=========

A tools to handle merging of
nested data structures in python.

------------
Installation
------------

deepmerge is available on `pypi <https://pypi.python.org/>`_:

.. code-block:: bash

   pip install deepmerge

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

Strategies are passed as a list, and the
merge runs through each strategy sequentially,
and raises an exception if none are able to resolve
the merge.

You can also pass in your own merge functions, instead of a string.
Your function should take the arguments of (``merger``, ``path``, ``base_value``, ``value_to_merge_in``).

A default merge does not exist, due to the
numerous choices that have to be made for every
merger. However, some very generic mergers are supplied:

* ``always_merger``: will never raise a merge exception, and
  will merge when possible.

* ``conservative_merger``: will never raise a merge exception and will use the original
  value when a conflict occurs.

* ``merge_or_raise``: will merge when possible, raise an exception
  when there is a conflict.

The best resource for now is the unit tests.
