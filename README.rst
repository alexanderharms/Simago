Simago: Population simulation
=============================

.. title-string

.. image:: https://github.com/alexanderharms/Simago/workflows/CI/badge.svg?branch=master
    :target: https://github.com/alexanderharms/Simago/actions?workflow=CI
    :alt: CI Status

.. image:: https://readthedocs.org/projects/simago/badge/?version=latest
    :target: https://simago.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

This package can be used to generate random populations, sets of microdata, based
on (publicly availabled) aggregated data.

These populations can then for example be used for experimentation in the field
of machine learning or simulation studies.

The package is available for Python 3 on `PyPI <https://pypi.org/project/simago/>`_,
the source code on `Github <https://github.com/alexanderharms/Simago>`_ and
the documentation on `ReadTheDocs <https://simago.readthedocs.io/en/latest/>`_.
The package is tested for Python 3.7 and up.

Usage
-----
The easiest way to get started, after installing the package with ``pip install simago``,
is to use the function ``generate_population()`` from ``simago.population``.
This function creates an instance of the ``PopulationClass`` object with
the generated population Pandas DataFrame as the ``PopulationClass.population``
attribute.

The population DataFrame contains a row for every person and a column for each
property. The values for these properties are randomly drawn from probability
distributions defined by the supplied data. This is done by supplying a
settings (YAML) file, a data (CSV) file and possibly a conditions (CSV) file.
For more guidance see the `example <https://simago.readthedocs.io/en/latest/example.html>`_
in the documentation.

How to contribute
-----------------
In order to contribute either leave a message in the Issues section or open a pull request.

Changelog
---------
.. include:: ./CHANGELOG.rst
   :start-after: last-version-start
   :end-before: last-version-end
