# -*- coding: utf-8 -*-
import unittest

import pint

import numpy as np
from numpy.testing import assert_allclose
from nose.tools import eq_

from hdf5plotter._util import (is_container, make_quantity, nested_iterable)


def test_is_container():
    input_output = (
        #input, output, message
        ([1, 2],            True, 'list'),
        ("Not a container", False, 'string'),
        (u"unicode not",    False, 'unicode'),
        (np.array([1, 2]),  True, 'array')
    )

    for input_, output, msg in input_output:
        eq_(is_container(input_), output, msg)


def test_make_quantity():
    u = pint.UnitRegistry()
    input_output = (
        ('nm', 1*u.nm, 'string to quantity'),
        (u.nm, 1*u.nm, 'quantity stays the same'),
    )

    for input_, exp_output, msg in input_output:
        output = make_quantity(input_)
        assert_allclose(output.magnitude, exp_output.magnitude, err_msg=msg)
        eq_(output.units, exp_output.units, msg)





def test_nested_iterable():
    input_output = (
        #input, output, message
        ([[1, 2], [3, 4]],                      True, "nested list"),
        ([1, 2],                                False, "list"),
        (np.array([1, 2, 3]),                   False, "array"),
        (np.array([[1, 2], [3, 4]]),            True, "2D array"),
        ([np.array([1, 2]), np.array([3, 4])],  True, "list of arrays"),
    )

    for input_, output, msg in input_output:
        eq_(nested_iterable(input_), output, msg)
