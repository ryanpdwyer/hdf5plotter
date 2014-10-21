# -*- coding: utf-8 -*-
from __future__ import division, print_function

import h5py
import matplotlib as mpl

from hdf5plotter import silent_del, u
from hdf5plotter._util import (replace_unit_label, replace_latex_label,
                               get_unit_attr)


class PlotFromManyFiles(object):
    """A prototype of a plottting class that plots one dataset from
    many files."""
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
        for group in self.groups:
            # Make sure the new dataset doesn't exist, so we can define it
            silent_del(group, new_dset)
            group.copy(old_dset, new_dset)
            old_unit = u(group[old_dset].attrs['unit'])
            scaled_dset = (group[old_dset][:] * old_unit).to(new_unit).magnitude
            group[new_dset][:] = scaled_dset
            new_attrs = group[new_dset].attrs
            new_attrs['unit'] = get_unit_attr(new_unit)
            new_attrs['label'] = replace_unit_label(
                new_attrs['label'], new_unit)
            new_attrs['label_latex'] = replace_latex_label(
                new_attrs['label_latex'], new_unit)


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