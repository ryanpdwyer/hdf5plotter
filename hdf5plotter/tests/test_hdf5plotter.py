# -*- coding: utf-8 -*-
import unittest
import h5py
import numpy as np
from numpy.testing import assert_array_equal


from hdf5plotter.tests import silentremove
from hdf5plotter import silent_del


class Test_silent_del(unittest.TestCase):
    filename = '.Test_silent_del.h5'

    def setUp(self):
        self.f = h5py.File(self.filename)
        self.f['exists'] = np.array([1, 2, 3, 4])

    def test_delete_exists(self):
        silent_del(self.f, 'exists')
        with self.assertRaises(KeyError):
            self.f['exists']

    def test_delete_doesnt_exist(self):
        silent_del(self.f, 'doesnt_exist')
        assert_array_equal(self.f['exists'][:], np.array([1, 2, 3, 4]))

    def tearDown(self):
        self.f.close()
        silentremove(self.filename)
