# -*- coding: utf-8 -*-
from __future__ import division, print_function

import h5py
import six
import re
import collections
import copy

import numpy as np
import pint

u = pint.UnitRegistry()

# Probably easier to get a list of all the attrs, then parse appropriately.


def h5ls_str(g, offset='', print_types=False):
    """Prints the input file/group/dataset (g) name and begin iterations on its
    content.

    See goo.gl/2JiUQK."""
    string = []
    if isinstance(g, h5py.File):
        string.append(offset+repr(g.file))
    elif isinstance(g, h5py.Dataset):
        if print_types:
            string.append(offset+g.name+'  '+repr(g.shape)+'  '+(g.dtype.str))
        else:
            string.append(offset+g.name+'  '+repr(g.shape))
    elif isinstance(g, h5py.Group):
        string.append(offset+g.name)
    else:
        raise ValueError('WARNING: UNKNOWN ITEM IN HDF5 FILE'+g.name)
    if isinstance(g, h5py.File) or isinstance(g, h5py.Group):
        for key, subg in dict(g).iteritems():
            string.append(h5ls_str(subg, offset + '    ',
                                   print_types=print_types))
    return "\n".join(string)


def h5ls(*args):
    """List the contents of an HDF5 file object or group.

    Accepts a file / group handle, or a string interpreted as the hdf5
    file path."""
    for arg in args:
        if isinstance(arg, six.string_types):
            fh = h5py.File(arg, mode='r')
            print(h5ls_str(fh))
            fh.close()
        else:
            print(h5ls_str(arg))


def create_attr_dictionary(f):
    d = {}

    def visitarg(key, ds):
        if isinstance(ds, h5py.Dataset):
            d[key] = dict(ds.attrs.items())

    f.visititems(visitarg)
    return d

permissive = {u'name', u'unit', u'label'}
latex = {u'name', u'unit', u'label', u'label_latex'}


def missing_attrs(attr_dictionary, attr_names):
    """Gives a dictionary of missing attributes"""
    mandatory = set(attr_names)
    missing_attrs = {}
    for ds_name, ds_attrs_dict in attr_dictionary.items():
        ds_attrs_keys = set(ds_attrs_dict.keys())
        missing_mandatory = mandatory.difference(ds_attrs_keys)
        if missing_mandatory:
            missing_attrs[ds_name] = tuple(missing_mandatory)
    return missing_attrs


def is_container(obj):
    """Check that an object is a container, but not a string."""
    return hasattr(obj, '__iter__') and not isinstance(obj, str)


def make_quantity(quantity_or_string):
    if isinstance(quantity_or_string, pint.compat.string_types):
        return u(quantity_or_string)
    else:
        return quantity_or_string

# TODO: Remove this ugly hack for pretty printing
# ------------------------------------------------------------------------
# This entire section is really repetitive, contains lots of duplicated work
def get_label_unit(quantity):
    q = make_quantity(quantity)
    return "".join(u"{0:P~}".format(q).split(' ')[1:]).replace('u', u'µ')


def get_unit_attr(quantity):
    q = make_quantity(quantity)
    return "".join(u"{0:~}".format(q).split(' ')[1:]).replace('**', '^')


def get_label_unit_substring(label):
    try:
        return re.search('[(\[][[\s\S]+[)\]]', label).group(0)[1:-1]
    except AttributeError:
        raise AttributeError("Could not find a unit substring in the label.")


def replace_unit_label_ascii(label, quantity):
    return label.replace(
        get_label_unit_substring(label), get_unit_attr(quantity))


def replace_unit_label(label, quantity):
    return label.replace(
        get_label_unit_substring(label), get_label_unit(quantity))


def replace_latex_label(label_latex, quantity):
    q = make_quantity(quantity)
    label_unit_substring = get_label_unit_substring(label_latex)
    new_label = "".join(u"{0:L~}".format(q).split(' ')[1:])
    substrings = re.findall('[a-zA-Z]+', new_label)
    for s in substrings:
        if s not in ('frac', 'sqrt'):
            if s.startswith('u'):
                new_label = new_label.replace(
                    s, "\\mu\\mathrm{{{s}}}".format(s=s[1:]))
            else:
                new_label = new_label.replace(s, "\\mathrm{{{s}}}".format(s=s))

    return label_latex.replace(label_unit_substring, new_label)
# ---------------------------------------------------------------------------


def iterable(x):
    """True if x is an iterable other than a string: some sort of list-like
    container"""
    # Not sure whether this works on Python3; does it capture both bytes and
    # unicode?
    if isinstance(x, str):
        return False
    else:
        return isinstance(x, collections.Iterable)


def nested_iterable(x):
    """Return true if x is (at least) list of lists, or a 2D numpy array, or
    list of 1D numpy arrays.

    Raises a TypeError if passed a non-iterable."""
    return all(iterable(i) for i in x)


def make_nested_array(x):
    if nested_iterable(x):
        return np.array(x)
    else:
        return np.array([x])


def replicate(x, y, magic):
    x = make_nested_array(x)
    y = make_nested_array(y)
    if magic is None:
        magic = np.array([magic])
    else:
        magic = np.array(magic)

    if len(y.shape) > 1:
        x_r = np.resize(x, y.shape)
        magic_r = np.resize(magic, y.shape[0])
    else:
        x_r = x
        magic_r = magic
    return zip(x_r, y, magic_r)


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
