# -*- coding: utf-8 -*-
import numpy as np
from nose.tools import eq_
from hdf5plotter._plot import plot


def test_plot():
    plot([1, 2, 3], [1, 4, 9])
