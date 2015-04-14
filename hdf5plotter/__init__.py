# -*- coding: utf-8 -*-
from __future__ import division, print_function
"""
HDF5 Plotter
============

This package defines some useful utility classes for gathering and processing
HDF5 files for plotting. A typical workflow involves selecting a few groups
for plotting from a few different HDF5 files, plotting the data with
some specifiec rcParams, and then adding

"""
__author__ = 'Ryan Dwyer'
__email__ = 'ryanpdwyer@gmail.com'
__version__ = '0.1.0'

import h5py
from hdf5plotter._util import silent_del, h5_list, update_attrs, u, h5ls
from hdf5plotter._plotters import PlotFromManyFiles


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
