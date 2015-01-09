# -*- coding: utf-8 -*-
from __future__ import division, print_function

import pint
import re

u = pint.UnitRegistry()


def is_container(obj):
    """Check that an object is a container, but not a string."""
    return hasattr(obj, '__iter__') and not isinstance(obj, str)


def make_quantity(quantity_or_string):
    if isinstance(quantity_or_string, pint.compat.string_types):
        return u(quantity_or_string)
    else:
        return quantity_or_string


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
