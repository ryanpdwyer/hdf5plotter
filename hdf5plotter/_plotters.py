# -*- coding: utf-8 -*-
from __future__ import division, print_function

import h5py
import matplotlib as mpl
from bunch import Bunch
import numpy as np
import pandas as pd


from hdf5plotter import silent_del, u, update_attrs
from hdf5plotter._util import (replace_unit_label, replace_latex_label,
                               get_unit_attr, is_container)


class PlotFromManyFiles(object):
    """A prototype of a plottting class that plots one dataset from
    many files."""
    def __init__(self):
        self.groups = []
        self.files = set()
        self.rcParams = {}

    def add(self, filename, group='/'):
        """Adds the group from filename, or a list of filenames,
        to the list of groups."""
        fh = h5py.File(filename)
        self.files.add(fh)
        self.add_group(fh[group])

    def add_group(self, h5_group):
        """Add group to the list of groups we are plotting."""
        self.groups.append(h5_group)

    def close(self):
        """Close open h5py files on delete."""
        for group in self.groups:
            group.file.close()

    def rescale(self, old_dset, new_dset, new_unit):
        """Rescale data in old_dset to the units new_unit, and put the result
        in a dataset named new_dset."""
        if new_dset == old_dset:
            raise ValueError("'new_dset' and 'old_dset' must be different.")
        for group in self.groups:
            # Calculate the new value
            old_unit = u(group[old_dset].attrs['unit'])
            scaled_dset = (group[old_dset][:] * old_unit).to(new_unit).magnitude
            if group.get(new_dset) is None:
                pass
            elif np.allclose(group.get(new_dset)[:], scaled_dset):
                break
            else:
                silent_del(group, new_dset)

            # Copy the dataset:
            group.copy(old_dset, new_dset)
            group[new_dset][:] = scaled_dset
            new_attrs = group[new_dset].attrs
            # Update the unit in the new_attrs
            new_attrs['unit'] = get_unit_attr(new_unit)
            new_attrs['label'] = replace_unit_label(
                new_attrs['label'], new_unit)
            new_attrs['label_latex'] = replace_latex_label(
                new_attrs['label_latex'], new_unit)

    def map(self, function, new_dset, new_attrs):
        """Transforms data using function, and puts the result in new_dset, and
        attachs the attributes new_attrs."""
        for group in self.groups:
            # Make sure the new dataset doesn't exist, so we can define it
            silent_del(group, new_dset)
            group[new_dset] = function(group)
            update_attrs(group[new_dset].attrs, new_attrs)

    def plot(self, x='x', y='y', scale='linear', shape='-', xlim=None, ylim=None,
            filename=None, save_fig_kwargs={}, store_fig=None):

        for key, val in self.rcParams.items():
            mpl.rcParams[key] = val

        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()

        plotting_functions = {
            'linear': ax.plot,
            'semilogy': ax.semilogy,
            'semilogx': ax.semilogx,
            'loglog': ax.loglog}

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

        if store_fig is not None:
            setattr(self, store_fig, Bunch(fig=fig, ax=ax))

        self.fig = fig
        self.ax = ax
        return fig, ax

    def to_DataFrame(self, datasets, index=0):
        """Return a DataFrame using the given datasets from id."""
        group = self.groups[index]
        data = np.r_[[group[dataset][:] for dataset in datasets]].T
        columns = [group[dataset].attrs['name'] for dataset in datasets]
        return pd.DataFrame(data=data, columns=columns)


