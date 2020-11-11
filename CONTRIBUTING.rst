How To Contribute
=================

Thank you for considering contributing to ``simago``! The power of open source
software is that we can together make something awesome. No contribution is
too small! If you would like to contribute, please submit an Issue or open
a pull request. In this document some guidelines are described for adding
code to the project.

Guidelines
----------
- Pretty basic, but the ground rule is 'Be nice to everybody'.
- When adding code to the project, add tests and documentation.
  For tests ``pytest`` is used and for documentation in the form
  of docstrings follow the Numpy docstring conventions.
- For pull requests into the ``master`` branch a CI pipeline in GitHub Actions
  is used. See in the CI section below for a description of the tests the
  code should pass. To make sure that the tests pass everytime it is handy to
  replicate the same setup when developing. The
  `blog post <https://hynek.me/talks/python-foss/>`_ written by Hynek
  Schlawack was a huge help for me.

Continuous integration (CI)
---------------------------
- Tests:

  - Framework used is ``pytest``, automated through ``tox``.
  - ``coverage`` is used to check test coverage; fails under 99%.
  - For tests in documentation ``doctest`` is used.
  - Tests are currently run in a Python 3.7 environment.

- Code quality:

  - Automated through ``pre-commit``. See ``.pre-commit-config.yaml`` to
    see the checks from ``pre-commit`` itself that are used.
  - ``isort`` is used to sort imports, ``flake8`` for static code analysis.
  - For correct packing ``MANIFEST.in`` is used; ``check-manifest`` is called
    through ``tox`` to check this file.

- Documentation:

  - Docstrings follow the Numpy docstring convention. Through ``pre-commit``
    ``interrogate`` is used to enforce a 95%+ docstring coverage.
  - Source files for documentation are written in reStructured Text (.rst)
    format and rendered with Sphinx. The documentation is published at
    ReadTheDocs.
