==========
Strategies
==========

Authoring your own Strategy
===========================

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


Note that the merger does not copy values before passing them into mergers for performance reasons.


Builtin Strategies
===========================

These are the built in strategies provided by deepmerge.


.. autoclass:: deepmerge.strategy.type_conflict.TypeConflictStrategies
    :members:
    :undoc-members:

.. autoclass:: deepmerge.strategy.fallback.FallbackStrategies
    :members:
    :undoc-members:

.. autoclass:: deepmerge.strategy.dict.DictStrategies
    :members:
    :undoc-members:

.. autoclass:: deepmerge.strategy.list.ListStrategies
    :members:
    :undoc-members:

List deduplication
~~~~~~~~~~~~~~~~~~

``append_unique`` compares values using Python equality, preserves existing
base-list duplicates, and appends only new incoming values. Equal dictionaries
are deduplicated even when nested dictionary insertion order or equal numeric
representations differ.

Built-in containers use structural hash buckets, with equality checks to handle
hash collisions. Custom objects, container subclasses, and recursive containers
use equality scans instead, including comparisons with indexed built-in values.
These fallback comparisons can take quadratic time. Values must not change during
the merge, and equality must return a usable boolean result. This does not add
support for objects whose equality raises an exception or returns an ambiguous
array result.
