#!/bin/bash
rm -rf build dist
cd docs
make html
cd ..
python3 -m pep517.build .
