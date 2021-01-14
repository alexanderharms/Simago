Changelog
=========

.. last-version-start

v0.3.2
^^^^^^

* Adds function ``adjust_filenames`` to ``simago.yamlutils``. Paths to data
  files should now either be defined as absolute paths or relative paths to
  the settings file.
* The example script from the ``example`` folder can now be called through
  ``python -m simago``, followed by the necessary arguments.
* Due to a (rather embarrasing) mistake in ``setup.py`` the actual code of
  the package was not put in the package on PyPI. That is fixed now.

.. last-version-end

v0.3.1
^^^^^^

* Small changes to metadata.

v0.3.0
^^^^^^

* Adds assertion to ``ContinuousProbabilityClass`` that checks that the
  specified function for the probability density function returns a frozen
  ``scipy.stats.rv_continuous`` object.
* Converts ``ProbabilityClass`` into an abstract base class and implements
  ``DiscreteProbabilityClass`` and ``ContinuousProbabilityClass``.
* Adds File Properties (``datafiles.rst``) to the documentation.
* What was previously names the 'conditionals file` will be from now on
  more aptly named the 'conditions file'.
* Automates testing and quality checking with ``tox``, ``coverage``,
  ``flake8``, ``isort``, ``pre-commit`` and ``interrogate``.
* Sets up documentation on ReadTheDocs and CI pipeline in Github Actions.
* Starts a changelog.
