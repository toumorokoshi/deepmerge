.. deepmerge documentation master file, created by
   sphinx-quickstart on Sun Nov 20 11:31:44 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Deepmerge: merging nested data structures
=========================================

Deepmerge is a flexible library to handle merging of
nested data structures in Python (e.g. lists, dicts).

It is available on `pypi <https://pypi.org/project/deepmerge/>`_, and
can be installed via pip:

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
            (dict, ["merge"]),
            (set, ["union"])
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

Want to get started? see the :doc:`./guide`

Contents:

.. toctree::
   :maxdepth: 2

   guide
   strategies
   api



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
