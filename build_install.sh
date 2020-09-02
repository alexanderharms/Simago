rm -rf build dist
cd docs
make html
cd ..
python3 -m pep517.build .

pip3 uninstall simago
pip3 install ./dist/simago-0.1.1-py3-none-any.whl
