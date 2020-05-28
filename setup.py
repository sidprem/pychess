from setuptools import setup
from Cython.Build import cythonize
# from setuptools.extension import Extension


# extensions = [
#     Extension('perft', ['perft.pyx'])
# ]

setup(
    ext_modules=cythonize("*.pyx"),
)
