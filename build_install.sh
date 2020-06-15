rm -rf build dist
python -m pep517.build .

pip uninstall simago
pip install ./dist/simago-0.1.0-py3-none-any.whl
