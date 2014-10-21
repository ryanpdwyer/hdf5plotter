# -*- coding: utf-8 -*-
from __future__ import division, print_function

import pint

u = pint.UnitRegistry()


def h5_list(f):
    def print_all(name):
        """Don't ever return a value, just none, so that we walk through
        all values of the file"""
        print(name)
        return None
    f.visit(print_all)


def silent_del(f, key):
    """Delete 'key' from the hdf5 file f, if it exists. If not, do nothing."""
    try:
        del f[key]
    except KeyError:
        pass


def update_attrs(attrs, dict_of_attrs):
    for key, val in dict_of_attrs.iteritems():
        attrs[key] = val
