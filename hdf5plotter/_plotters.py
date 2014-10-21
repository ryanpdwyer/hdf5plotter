# -*- coding: utf-8 -*-
from __future__ import division, print_function

import h5py
import matplotlib as mpl


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

    def rescale(self, old_dset, new_dset, new_unit):
        pass

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