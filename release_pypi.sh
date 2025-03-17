#!/usr/bin/env bash

if [[ -z "${INTERP}" ]]; then
  INTERP=python
fi

echo "Removing previous build artifacts"
rm -f dist/*

echo "Building source distribution.."
$INTERP -m build

echo "Uploading to PyPI.."
$INTERP -m twine upload dist/*

echo "Finished."
