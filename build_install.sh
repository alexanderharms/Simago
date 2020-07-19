rm -rf build dist
cd docs
make html
cd ..
python -m pep517.build .

pip uninstall simago
pip install ./dist/simago-0.1.1-py3-none-any.whl
