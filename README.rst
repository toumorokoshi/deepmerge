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

**Generic Strategy**

.. code-block:: python

    from deepmerge import always_merger

    base = {"foo": ["bar"]}
    next = {"foo": ["baz"]}

    expected_result = {'foo': ['bar', 'baz']}
    result = always_merger.merge(base, next)

    assert expected_result == result


**Custom Strategy**

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


You can also pass in your own merge functions, instead of a string.
Your function should take the arguments of (``merger``, ``path``, ``base_value``, ``value_to_merge_in``).

Strategies are passed as a list, and the
merge runs through each strategy in the order passed into the merger,
stopping at the first one to return a value that is not
the sentinel value deepmerge.STRATEGY_END.

For example, this function would not be considered valid for any base value besides the string "foo":

.. code-block:: python
  from deepmerge import STRATEGY_END

  def return_true_if_foo(config, path, base, nxt):
    if base == "foo":
        return True
    return STRATEGY_END


Note that strategies should not modify base or nxt. The Merger does not copy values before passing them into mergers for performance reasons.

Available Merge Strategies
**************************

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

-----
Tests
-----

.. code-block:: shell

    $ pip install pytest
    $ pytest deepmerge/tests/
