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

class PlotFromManyFiles(object):
    """A prototype of a plottting class that plots one dataset from many files."""
    def __init__(self):
        self.groups = []
        self.rcParams = {}

    def add(self, filename, group='/'):
        """Adds the group from filename to the """
        fh = h5py.File(filename)
        self.groups.append(fh)

    def __del__(self):
        """Close open h5py files on delete."""
        for group in self.groups:
            group.file.close()

    def plot(self, x='x', y='y', scale='linear', shape='-', xlim=None, ylim=None,
             rcParams=None, filename=None, save_fig_kwargs={}):
        if rcParams is not None:
            self.rcParams = rcParams
        for key, val in self.rcParams.items():
            mpl.rcParams[key] = val

        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()

        plotting_functions = OrderedDict((
        ('linear', ax.plot),
        ('semilogy', ax.semilogy),
        ('semilogx', ax.semilogx),
        ('loglog', ax.loglog)))

        plot = plotting_functions[scale]

        for group in self.groups:
            line = plot(group[x].value, group[y].value, shape)

        ax.set_xlabel(group[x].attrs['label'])
        ax.set_ylabel(group[y].attrs['label'])

        if xlim is not None:
            ax.set_xlim(xlim)
        if ylim is not None:
            ax.set_ylim(ylim)

        fig.canvas.draw()

        if filename is not None:
            fig.savefig(filename, **save_fig_kwargs)

        self.fig = fig
        self.ax = ax
        return fig, ax


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


def make_uF_array(plotter):
    attrs = OrderedDict((
        (u'unit', u'F/µm^2'),
        (u'name', "C''(z)"),
        (u'label', u"C''(z) [µF/m\u00B2]"),
        (u'label_latex', '$C_2(z) [\\mu \\mathrm{F}/\\mathrm{m}^2]$'),
        (u'help',
          'Second derivative of the capacitance,\ncalculated from a frequency parabola\nand the cantilever spring constant.'),
        (u'n_avg', 1.0)))
    for group in plotter.groups:
        try:
            del group['y2_uF']
        except KeyError:
            pass
        group['y2_uF'] = group['y2'].value*1e6
        update_attrs(group['y2_uF'].attrs, attrs)

def make_uF_array(plotter):
    attrs = OrderedDict((
        (u'unit', u'F/µm^2'),
        (u'name', "C''(z)"),
        (u'label', u"C''(z) [µF/m\u00B2]"),
        (u'label_latex', '$C_2(z) [\\mu \\mathrm{F}/\\mathrm{m}^2]$'),
        (u'help',
          'Second derivative of the capacitance,\ncalculated from a frequency parabola\nand the cantilever spring constant.'),
        (u'n_avg', 1.0)))
    for group in plotter.groups:
        try:
            del group['y3_uF']
        except KeyError:
            pass
        group['y3_uF'] = group['y3'].value*1e6
        update_attrs(group['y3_uF'].attrs, attrs)

def make_gamma(plotter):
    attrs = OrderedDict((
    (u'unit', u'pN s/m'),
    (u'name', "Friction"),
    (u'label', u"Friction [pNs/m]"),
    (u'label_latex', 'Friction $\\Gamma \\: [\\mathrm{pN} \\mathrm{s}/\\mathrm{m}]$'),
    (u'help', """Measured friction,
calculated from the cantilever spring constant
(calculated from Brownian motion), resonance frequency,
quality factor (calculated from ring-down)"""),
    (u'n_avg', 1.0)))
    # See Ryan's notebook, September 2014 for more information about
    # the cantilever this data was taken with:
    # 2014-09-10-DPE18/noAl-75kHz-3.5N/m
    f_c = 61300
    k_c = 2.5
    for group in plotter.groups:
        try:
            Gamma = group['Gamma']
        except:
            group['Gamma'] = np.zeros(np.array(group['y'][:]).size)
            Gamma = group['Gamma']
        
        Q = group['y'][:]
        Gamma[:] = k_c / (f_c * 2 * np.pi * Q) * 1e12
        update_attrs(Gamma.attrs, attrs)
            
    
def make_Gamma_s(plotter, gamma_i):
    attrs = OrderedDict((
    (u'unit', u'pN s/m'),
    (u'name', "Sample-induced Friction"),
    (u'label', u"Friction [pNs/m]"),
    (u'label_latex', 'Friction $\\Gamma_{\\mathrm{s}} \\: [\\mathrm{pN} \\mathrm{s}/\\mathrm{m}]$'),
    (u'help', """Sample induced friction, calculated by subtracting an intrinsic dissipation."""),
    (u'Gamma_i', gamma_i)))
    for group in plotter.groups:
        Gamma = group['Gamma']
        try:
            Gamma_s = group['Gamma_s']
        except:
            group['Gamma_s'] = np.zeros(np.array(group['y'][:]).size)
            Gamma_s = group['Gamma_s']
        
        Gamma_s[:] = Gamma[:] - gamma_i
        update_attrs(Gamma_s.attrs, attrs)
    
def make_z(plotter):
    calibration = 50  # nm / V
    attrs = OrderedDict((
    (u'unit', u'nm'),
    (u'name', "d"),
    (u'label', u"Distance [nm]"),
    (u'label_latex', '$d \\: [\\mathrm{pN} \\mathrm{s}/\\mathrm{m}]$'),
    (u'help', """Distance between cantilever and surface."""),
    (u'Z Piezo Calibration [nm/V]', calibration)))
    # See Ryan's notebook, September 2014 for more information about
    # the cantilever this data was taken with:
    # 2014-09-10-DPE18/noAl-75kHz-3.5N/m
    for group in plotter.groups:
        x = group['x'][:]
        try:
            z = group['d']
        except:
            group['d'] = np.zeros(x.size)
            z = group['d']
        
        z[:] = x * 50
        update_attrs(z.attrs, attrs)
