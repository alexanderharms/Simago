# Build Python package
build_package:
	rm -rf build dist
	python3 -m pep517.build .
# Check if tests pass with tox
# Etc.
