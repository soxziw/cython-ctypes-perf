"""
Setup script for building Cython extensions and C library
"""

from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np
import os

# C library source files
c_sources = ['src/benchmark_lib.c']

# Cython extension
cython_extensions = [
    Extension(
        "cython_wrapper",
        sources=["src/cython_wrapper.pyx"] + c_sources,
        include_dirs=[np.get_include(), "src"],
        extra_compile_args=['-O3', '-march=native', '-fPIC'],
        language="c"
    )
]

setup(
    name="cython-ctypes-perf",
    version="1.0.0",
    description="Performance comparison of Cython vs ctypes FFI",
    ext_modules=cythonize(
        cython_extensions,
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
            'cdivision': True,
            'embedsignature': True
        }
    ),
    zip_safe=False,
)

