#!/bin/bash -e

pip uninstall axelerate
python setup.py clean
rm -rf build/*
# python setup.py build
python setup.py develop