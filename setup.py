#!/usr/bin/env python

import os
import sys

from setuptools import setup

# See https://github.com/warner/python-versioneer
import versioneer
versioneer.VCS = 'git'
versioneer.versionfile_source = 'hdf5plotter/_version.py'
versioneer.versionfile_build = 'hdf5plotter/_version.py'
versioneer.tag_prefix = '' # tags are like 1.2.0
versioneer.parentdir_prefix = 'hdf5plotter-' # dirname like 'myproject-1.2.0'

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://hdf5plotter.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='hdf5plotter',
    version=versioneer.get_version(),
    description='Plot data contained in HDF5 files.',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Ryan Dwyer',
    author_email='ryanpdwyer@gmail.com',
    url='https://github.com/ryanpdwyer/hdf5plotter',
    packages=[
        'hdf5plotter'
    ],
    include_package_data=True,
    install_requires=['numpy', 'scipy', 'matplotlib', 'h5py', 'pint', 'bunch',
    'pandas', 'click', 'seaborn', 'pathlib'],
    tests_require=['nose>=1.0'],
    test_suite='nose.collector',
    license='MIT',
    zip_safe=False,
    cmdclass=versioneer.get_cmdclass(),
    entry_points="""
        [console_scripts]
        h5plot=hdf5plotter._cli:cli
        csvplot=hdf5plotter._cli:csvplot
        csvscale=hdf5plotter._cli:csvscale
    """,
    keywords='hdf5plotter',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ]
)
