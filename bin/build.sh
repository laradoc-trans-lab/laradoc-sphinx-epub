#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

echo ">>> Cleaning previous builds..."
rm -Rf build/color/*
rm -Rf build/color/.buildinfo*
rm -Rf build/color/.doctrees
rm -Rf build/grayscale/*
rm -Rf build/grayscale/.buildinfo*
rm -Rf build/grayscale/.doctrees

echo ">>> Pre processing source files..."
python3 bin/preprocess_docs.py source book/source

cd book

echo ">>> Building EPUB (color version) with Sphinx..."
SPHINX_CUSTOM_CONFIG="color" sphinx-build -E -a -b epub  --conf-dir . source ../build/color

echo ">>> Building EPUB (grayscalebw version) with Sphinx..."
SPHINX_CUSTOM_CONFIG="grayscale" sphinx-build -E -a -b epub --conf-dir .  source ../build/grayscale

echo ">>> Build complete! Check the 'output' directory."
