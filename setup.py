"""
Setup file for package `simobject`.
"""
from setuptools import setup
import pathlib

PACKAGENAME = 'simobject'

# the directory where this setup.py resides
HERE = pathlib.Path(__file__).absolute().parent


def read_version():
    with (HERE / PACKAGENAME / '__init__.py').open() as fid:
        for line in fid:
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
        else:
            raise RuntimeError("Unable to find version string.")


if __name__ == "__main__":

    setup(
        name=PACKAGENAME,
        description='simple basic framework for a simulation',
        version=read_version(),
        long_description=(HERE / "Readme.rst").read_text(),
        long_description_content_type='text/x-rst',
        url='https://github.com/birnstiel/simobject',
        author='Til Birnstiel',
        author_email='til.birnstiel@lmu.de',
        license='GPLv3',
        packages=[PACKAGENAME],
        package_dir={PACKAGENAME: PACKAGENAME},
        install_requires=[
            'pytest',
            'numpy'],
        zip_safe=True,
    )
