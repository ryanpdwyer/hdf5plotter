#!/usr/bin/env python

import os
import sys


from setuptools import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://hdf5plotter.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='hdf5plotter',
    version='0.1.0',
    description='Plot data contained in HDF5 files.',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Ryan Dwyer',
    author_email='ryanpdwyer@gmail.com',
    url='https://github.com/ryanpdwyer/hdf5plotter',
    packages=[
        'hdf5plotter'
    ],
    include_package_data=True,
    install_requires=['numpy', 'matplotlib', 'h5py', 'pint'],
    tests_require=['nose>=1.0'],
    test_suite='nose.collector',
    license='MIT',
    zip_safe=False,
    keywords='hdf5-plotter',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ]
)
