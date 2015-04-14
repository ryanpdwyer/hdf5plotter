# -*- coding: utf-8 -*-
import unittest
from collections import OrderedDict
import h5py
import numpy as np
from numpy.testing import assert_array_equal, assert_array_max_ulp
from nose.tools import eq_


from hdf5plotter.tests import silentremove
from hdf5plotter import silent_del, update_attrs, PlotFromManyFiles, u


def create_sample_h5_file(filename):
    f = h5py.File(filename)
    f['x'] = np.arange(0, 10, 0.1, dtype=np.float64)
    f['y'] = 100*np.sin(f['x'][:])
    x_attrs = OrderedDict(((u'name', "Time"),
                          (u'unit', u'ms'),
                          (u'label', u"Time [ms]"),
                          (u'label_latex', u'Time $t \\: [\\mathrm{ms}]$'),
                          (u'help', u'Time example')))
    update_attrs(f['x'].attrs, x_attrs)

    y_attrs = OrderedDict(((u'name', "Displacement Squared"),
                          (u'unit', u'nm^2'),
                          (u'label', u"z [nm\xb2]"),
                          (u'label_latex', u'$z \\: [\\mathrm{nm}^2]$'),
                          (u'help', u'Displacement example'),
                          (u'n_avg', 1.0)))
    update_attrs(f['y'].attrs, y_attrs)
    f.close()


class Test_silent_del(unittest.TestCase):
    filename = '.Test_silent_del.h5'

    def setUp(self):
        silentremove(self.filename)
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


class TestPlotFromManyFiles_init(unittest.TestCase):
    filename = '.TestPlotFromManyFiles_init.h5'

    def setUp(self):
        silentremove(self.filename)
        self.f = h5py.File(self.filename)
        self.f['x'] = np.arange(0, 10, 0.1, dtype=np.float64)
        self.f['y'] = 100*np.sin(self.f['x'][:])
        x_attrs = OrderedDict(((u'name', "Time"),
                              (u'unit', u'ms'),
                              (u'label', u"Time [ms]"),
                              (u'label_latex', u'Time $t \\: [\\mathrm{ms}]$'),
                              (u'help', u'Time example')))
        update_attrs(self.f['x'].attrs, x_attrs)

        y_attrs = OrderedDict(((u'name', "Displacement"),
                              (u'unit', u'nm'),
                              (u'label', u"z [nm]"),
                              (u'label_latex', u'$z \\: [\\mathrm{nm}]$'),
                              (u'help', u'Displacement example'),
                              (u'n_avg', 1.0)))
        update_attrs(self.f['y'].attrs, y_attrs)
        self.f.close()
        del self.f

    def test__init__(self):
        self.plotter = PlotFromManyFiles()

    def test_add(self):
        self.plotter = PlotFromManyFiles()
        self.plotter.add(self.filename)
        print(self.plotter.groups)

    def tearDown(self):
        self.plotter.close()
        silentremove(self.filename)


class TestPlotFromManyFiles_rescale(unittest.TestCase):
    filename = '.TestPlotFromManyFiles_rescale.h5'

    def setUp(self):
        silentremove(self.filename)
        self.f = h5py.File(self.filename)
        self.f['x'] = np.arange(0, 10, 0.1, dtype=np.float64)
        self.f['y'] = 100*np.sin(self.f['x'][:])
        x_attrs = OrderedDict(((u'name', "Time"),
                              (u'unit', u'ms'),
                              (u'label', u"Time [ms]"),
                              (u'label_latex', u'Time $t \\: [\\mathrm{ms}]$'),
                              (u'help', u'Time example')))
        update_attrs(self.f['x'].attrs, x_attrs)

        y_attrs = OrderedDict(((u'name', "Displacement Squared"),
                              (u'unit', u'nm^2'),
                              (u'label', u"z [nm\xb2]"),
                              (u'label_latex', u'$z \\: [\\mathrm{nm}^2]$'),
                              (u'help', u'Displacement example'),
                              (u'n_avg', 1.0)))
        update_attrs(self.f['y'].attrs, y_attrs)

        self.plotter = PlotFromManyFiles()
        self.plotter.add(self.filename)

    def test_rescale_normal(self):
        x_sec = self.f['x'][:] / 1000
        self.plotter.rescale('x', 'x_s', 's')
        assert_array_max_ulp(self.plotter.groups[0]['x_s'][:], x_sec, 5)

        x_s_attrs = self.f['x_s'].attrs

        exp_x_s_attrs = OrderedDict((
            (u'name', "Time"),
            (u'unit', u's'),
            (u'label', u"Time [s]"),
            (u'label_latex', u'Time $t \\: [\\mathrm{s}]$'),
            (u'help', u'Time example')))

        for key, val in exp_x_s_attrs.items():
            eq_(val, x_s_attrs[key])

    def test_rescale_twice(self):
        x_sec = self.f['x'][:] / 1000
        self.plotter.rescale('x', 'x_s', 's')
        # Rescale twice; make sure the rescale function can handle this
        self.plotter.rescale('x', 'x_s', 's')
        
        assert_array_max_ulp(self.plotter.groups[0]['x_s'][:], x_sec, 5)

        x_s_attrs = self.f['x_s'].attrs

        exp_x_s_attrs = OrderedDict((
            (u'name', "Time"),
            (u'unit', u's'),
            (u'label', u"Time [s]"),
            (u'label_latex', u'Time $t \\: [\\mathrm{s}]$'),
            (u'help', u'Time example')))

        for key, val in exp_x_s_attrs.items():
            eq_(val, x_s_attrs[key])

    def test_rescale_different_units(self):
        x_s = self.f['x'][:] * 1000000
        self.plotter.rescale('x', 'x_s', 's')
        # Rescale twice; make sure the rescale function can handle this
        self.plotter.rescale('x', 'x_s', 'ns')
        
        assert_array_max_ulp(self.plotter.groups[0]['x_s'][:], x_s, 5)

        x_s_attrs = self.f['x_s'].attrs

        exp_x_s_attrs = OrderedDict((
            (u'name', "Time"),
            (u'unit', u'ns'),
            (u'label', u"Time [ns]"),
            (u'label_latex', u'Time $t \\: [\\mathrm{ns}]$'),
            (u'help', u'Time example')))

        for key, val in exp_x_s_attrs.items():
            eq_(val, x_s_attrs[key])

    def test_rescale_squared_micro_prefix(self):
        y_um = self.f['y'][:] / 1000**2
        self.plotter.rescale('y', 'y_um', u.um**2)
        assert_array_max_ulp(self.plotter.groups[0]['y_um'][:], y_um, 10)
        y_um_attrs = self.f['y_um'].attrs
        exp_y_um_attrs = OrderedDict((
            (u'name', "Displacement Squared"),
            (u'unit', u'um^2'),
            (u'label', u"z [\xb5m\xb2]"),
            (u'label_latex', u'$z \\: [\\mu\\mathrm{m}^{2}]$'),
            (u'help', u'Displacement example'),
            (u'n_avg', 1.0)))

        for key, val in exp_y_um_attrs.items():
            eq_(val, y_um_attrs[key])

    def tearDown(self):
        self.plotter.close()
        silentremove(self.filename)


class TestPlotFromManyFiles_map(unittest.TestCase):
    filename = '.TestPlotFromManyFiles_map.h5'

    def setUp(self):
        silentremove(self.filename)
        self.f = h5py.File(self.filename)
        self.f['x'] = np.arange(0, 10, 0.1, dtype=np.float64)
        self.f['y'] = 100*np.sin(self.f['x'][:])
        x_attrs = OrderedDict(((u'name', "Time"),
                              (u'unit', u'ms'),
                              (u'label', u"Time [ms]"),
                              (u'label_latex', u'Time $t \\: [\\mathrm{ms}]$'),
                              (u'help', u'Time example')))
        update_attrs(self.f['x'].attrs, x_attrs)

        y_attrs = OrderedDict(((u'name', "Displacement Squared"),
                              (u'unit', u'nm^2'),
                              (u'label', u"z [nm\xb2]"),
                              (u'label_latex', u'$z \\: [\\mathrm{nm}^2]$'),
                              (u'help', u'Displacement example'),
                              (u'n_avg', 1.0)))
        update_attrs(self.f['y'].attrs, y_attrs)

        self.plotter = PlotFromManyFiles()
        self.plotter.add(self.filename)

    def test_square_root_y(self):

        new_attrs = OrderedDict((
            (u'name', "Displacement"),
            (u'unit', u'nm'),
            (u'label', u"z [nm]"),
            (u'label_latex', u'$z \\: [\\mathrm{nm}]$'),
            (u'help', u'Displacement example'),
            (u'n_avg', 1.0)))

        exp_y_sqrt = 10*np.sqrt(np.abs(np.sin(self.f['x'][:])))

        def transform(group):
            return np.abs(group['y'][:])**0.5

        self.plotter.map(transform, 'y_sqrt', new_attrs)

        y_sqrt = self.plotter.groups[0]['y_sqrt']

        assert_array_max_ulp(exp_y_sqrt, y_sqrt[:], 5)

        for key, val in new_attrs.items():
            eq_(val, y_sqrt.attrs[key])

    def tearDown(self):
        self.plotter.close()
        silentremove(self.filename)


class TestPlotFromManyFiles_to_DataFrame(unittest.TestCase):
    filename = '.TestPlotFromManyFiles_to_DataFrame.h5'

    def setUp(self):
        silentremove(self.filename)
        self.f = h5py.File(self.filename)
        self.f['x'] = np.arange(0, 10, 0.1, dtype=np.float64)
        self.f['y'] = 100*np.sin(self.f['x'][:])
        x_attrs = OrderedDict(((u'name', "Time"),
                              (u'unit', u'ms'),
                              (u'label', u"Time [ms]"),
                              (u'label_latex', u'Time $t \\: [\\mathrm{ms}]$'),
                              (u'help', u'Time example')))
        update_attrs(self.f['x'].attrs, x_attrs)

        y_attrs = OrderedDict(((u'name', "Displacement"),
                              (u'unit', u'nm'),
                              (u'label', u"z [nm]"),
                              (u'label_latex', u'$z \\: [\\mathrm{nm}]$'),
                              (u'help', u'Displacement example'),
                              (u'n_avg', 1.0)))
        update_attrs(self.f['y'].attrs, y_attrs)

        self.plotter = PlotFromManyFiles()
        self.plotter.add(self.filename)

    def test_to_dataframe(self):
        df = self.plotter.to_DataFrame(['x', 'y'], index=0)
        group = self.plotter.groups[0]
        assert_array_max_ulp(group['x'][:], df['Time'].values)
        assert_array_max_ulp(group['y'][:], df['Displacement'].values)

    def tearDown(self):
        self.plotter.close()
        silentremove(self.filename)
