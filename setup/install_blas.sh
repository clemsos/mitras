#!/bin/bash
workon [envname]
pip uninstall numpy ## only if numpy is already installed
pip uninstall scipy ## only if scipy is already installed
export LAPACK=/usr/lib/liblapack.so
export ATLAS=/usr/lib/libatlas.so
export BLAS=/usr/lib/libblas.so
