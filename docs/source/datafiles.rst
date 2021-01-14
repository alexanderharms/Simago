File properties
===============

The settings and data in order to generate a random population are determined
by three types of files. On this page more information is given about these
files. For an example of the ``simago`` package in use, see the Example page.

Settings (YAML) file
-----------------------

In this section the possible variables of the settings (YAML) files can
are discussed. The validity of these rules are checked by the function
``simago.yamlutils.check_yaml``. The settings files should have a valid YAML
syntax and the extenstions ``.yml`` or ``.yaml``. All file paths in the
settings files should be either absolute paths or relative paths to the
settings file.

* ``property_name`` (essential): Name of the (random) property of the persons.
  Entries for ``property_name`` should be unique strings.
* ``data_type`` (essential): Type of the data of the property.
  Entries for ``data_type`` should be either ``categorical``, ``ordinal`` or
  ``continuous``, for data that is discrete without ordering, discrete with
  ordering or continous in nature respectively.
* ``data_file`` (essential if ``data_type`` is ``categorical`` or
  ``ordinal``): File containing the number of people corresponding to each
  discrete category. These numbers are normalized to form the discrete
  probability distribution. Entries for ``data_file`` should be strings
  for the filenames of the CSV files containing the data.
* ``pdf_file`` (essential if ``data_type`` is ``continuous``): Filename
  of the Python file in which the PDF (probability density function) is defined
  for the continuous probability distribution.
* ``pdf`` (essential if ``data_type`` is ``continuous``): String
  of the function name defined in ``pdf_file`` that produces the PDF for
  the continuous property. This function should return a 'frozen'
  ``scipy.stats.rv_continuous`` object. This object becomes frozen when it is
  initialized with specified parameters for its probability distribution.
* ``pdf_parameters`` (essential if ``data_type`` is ``continuous``):
  A list of parameters for the PDF function. Each position in the list
  corresponds to the equivalent condition index in the conditions file.
* ``conditions``: File containing the conditions for the conditional
  probability distributions. Entries for ``conditions`` should be strings
  for the filenames of the CSV files containing the data. If an entry is not
  supplied this variable is set to ``None``.

Data file
---------

The data file is a CSV file containing the data for the discrete probability
distributions. This is the case when ``data_type`` is ``categorical`` or
``ordinal``.  This file should have the following columns:

* ``option``: Index for the possibilities in the probability distributions.
* ``value``: The number of people corresponding to each ``option``.
* ``label``: A human readable label for each ``option``. Only used
  when exporting the population.
* ``condition_index``: Index corresponding to the conditions defined in
  the conditions file.

Conditions file
---------------

The conditions file is a CSV file containing the conditions for the
conditional probability distributions. Each condition is defined by
the ``relation`` to the ``option`` of an already defined ``property_name``.
For example, an age distribution for males would only hold for the people
for which ``property_name`` ``sex`` is equal, ``relation`` is ``eq``, to the
``option`` ``0`` if ``0`` is defined as male. This file should have the
following columns:

* ``condition_index``: Index for the conditional probability distribution.
  This index should match the ``condition_index`` defined in the data file in
  the case of a discrete probability distribution or the position in the list of
  parameters defined in the variable ``pdf_parameters`` in the settings file for
  a continuous probability distribution.
* ``property_name``: Name of the property which determines the condition.
* ``option``: Option of the property.
* ``relation``: Relation to the ``option``. For ``categorical`` data only
  ``eq`` or ``neq`` should be used. Entries for ``relation`` can be

  * ``eq`` for 'equal to'
  * ``neq`` for 'not equal to'
  * ``leq`` for 'lesser than or equal to'
  * ``geq`` for 'greater than or equal to'
  * ``le`` for 'less than'
  * ``gr`` for 'greater than'.
