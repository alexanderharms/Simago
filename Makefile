# Build Python package
# In order to build the package:
# The tests must pass an must have the correct coverage
# The doctests must pass
# Pre-commit must pass
# - Sort with isort
# - flake8 must pass
# check-manifest must pass
# Documentation must be built.
# Correct version number?
# Is the changelog updated?

# After building the package:
# The PyPI description must pass twine
# Test if the packages install correctly
# Commit the changes & tag the version

# Uploading the package to test-PyPI

# Uploading the package to production-PyPI

package: pre_build build_package post_build clean

build_package: pre_build
	rm -rf build dist
	make_env/bin/python -m pep517.build --source --binary .
	ls -l dist

setup_makefile:
	rm -rf make_env
	python3 -m venv make_env
	make_env/bin/pip install tox pre-commit sphinx twine pep517

pre_build: run_tests check_version_number check_changelog build_docs

post_build: twine_check check_install_sdist check_install_wheel generate_example

run_tests: setup_makefile
	make_env/bin/python -m tox
	make_env/bin/python -m tox -e docs,manifest,precommit

check_version_number:
	@echo "Is the version number correct?"

check_changelog:
	@echo "Is the changelog updated?"

build_docs: setup_makefile
	make_env/bin/python make_env/bin/sphinx-build -W -b html -d docs/doctrees docs/source docs/_build/html

twine_check: setup_makefile
	make_env/bin/python -m twine check dist/*

check_install_sdist:
	rm -rf venv-sdist
	python3 -m venv venv-sdist
	venv-sdist/bin/pip install dist/simago-*.tar.gz
	venv-sdist/bin/python -c "import simago; print(simago.__version__)"
	rm -rf venv-sdist

check_install_wheel:
	rm -rf venv-wheel
	python3 -m venv venv-wheel
	venv-wheel/bin/pip install dist/simago-*.whl
	venv-wheel/bin/python -c "import simago; print(simago.__version__)"
	rm -rf venv-wheel

check_install_pypi_test:
	rm -rf venv-pypi-test
	python3 -m venv venv-pypi-test
	venv-pypi-test/bin/pip install -i https://test.pypi.org/simple/ simago
	venv-pypi-test/bin/python -c "import simago; print(simago.__version__)"
	rm -rf venv-pypi-test

check_install_pypi:
	rm -rf venv-pypi
	python3 -m venv venv-pypi
	venv-pypi/bin/pip install simago
	venv-pypi/bin/python -c "import simago; print(simago.__version__)"
	rm -rf venv-pypi

upload_pypi_test:
	@echo "To be implemented"

upload_pypi_prod:
	@echo "To be implementend"

generate_example:
	rm -rf example_env
	python3 -m venv example_env
	example_env/bin/pip install ./dist/simago-*.whl
	example_env/bin/python -m simago -p 1000 \
	--yaml_folder ./example/data-yaml/ \
	-o ./example/output/population.csv \
	--rand_seed 100
	rm -rf example_env

clean:
	rm -rf make_env
	rm -rf venv-sdist
	rm -rf venv-wheel
	rm -rf venv-pypi-test
	rm -rf venv-pypi
