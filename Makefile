# Build Python package
build_package:
	rm -rf build dist
	python3 -m pep517.build .

# In order to build the package:
# The tests must pass an must have the correct coverage
# The doctests must pass
# Pre-commit must pass
# - Sort with isort
# - flake8 must pass
# check-manifest must pass
# Correct version number?
# Is the changelog updated?
# Documentation must be built.

# After building the package:
# The PyPI description must pass twine
# Test if the packages install correctly
# Commit the changes & tag the version

# Uploading the package to test-PyPI

# Uploading the package to production-PyPI
