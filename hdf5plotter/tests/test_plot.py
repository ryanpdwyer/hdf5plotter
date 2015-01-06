# -*- coding: utf-8 -*-
import unittest
import numpy as np
from nose.tools import eq_
from hdf5plotter._plot import nested_iterable, plot

def test_nested_iterable():
    input_output = (
        #input, output, message
        ([[1, 2], [3, 4]], True, "nested list"),
        ([1, 2], False, "list"),
        (np.array([1, 2, 3]), False, "array"),
        (np.array([[1,2], [3, 4]]), True, "2D array"),
        ([np.array([1, 2]), np.array([3, 4])], True, "list of arrays"),
        )

    for input_, output, msg in input_output:
        eq_(nested_iterable(input_), output, msg)


def test_plot():
    plot([1, 2, 3], [1, 4, 9])
