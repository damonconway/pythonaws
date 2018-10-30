#!/bin/sh
#
# $Id$

echo "Running pycodestyle"
pycodestyle --ignore=E501 webotron/
echo "Running pydocstyle"
pydocstyle webotron/
echo "Running pylint"
pylint webotron/
echo "Running pyflakes"
pyflakes webotron/
