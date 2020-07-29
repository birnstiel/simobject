"""
Setup file for package `simobject`.
"""
from setuptools import setup
import pathlib

PACKAGENAME = 'simobject'

# the directory where this setup.py resides
HERE = pathlib.Path(__file__).parent

if __name__ == "__main__":

    setup(
        name=PACKAGENAME,
        description='simple basic framework for a simulation',
        version='0.0.1',
        long_description=(HERE / "Readme.md").read_text(),
        long_description_content_type='text/markdown',
        url='til-birnstiel.de',
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
