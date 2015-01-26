# -*- coding: utf-8 -*-
import matplotlib as mpl
import matplotlib.pyplot as plt

from hdf5plotter._util import replicate

"""Expectation:
plot(x=[1, 2, 3], y=[1, 4, 9])
plot(x=[[1, 2, 3], [1, 1.5, 2, 2.5, 3]], y=[[1, 4, 9], [1, 2, 4, 6, 9]])

"""


def plot(x, y, magic=None, scale='linear', xlabel=None, ylabel=None, shape=None,
         xlim=None, ylim=None, rcParams={'backend': 'Qt4Agg'}, **plot_kwargs):
    """A all in one plotting function which adds scale, labels, limits, shape,
    and the option to specify additional parameters."""
    with mpl.rc_context(rc=rcParams):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        plotting_functions = {
            'linear': ax.plot,
            'semilogy': ax.semilogy,
            'semilogx': ax.semilogx,
            'loglog': ax.loglog}

        plot_scale_func = plotting_functions[scale]

        def plot_single(x, y, magic, plot_kwargs):
            if magic is None:
                return plot_scale_func(x, y, **plot_kwargs)
            else:
                return plot_scale_func(x, y, magic, **plot_kwargs)

        for xi, yi, mi in replicate(x, y, magic):
            plot_single(xi, yi, mi, plot_kwargs)

        if xlabel is not None:
            ax.set_xlabel(xlabel)
        if ylabel is not None:
            ax.set_ylabel(ylabel)

        if xlim is not None:
            ax.set_xlim(xlim)
        if ylim is not None:
            ax.set_ylim(ylim)

        # fig.tight_layout alone was causing problems.
        # See https://github.com/matplotlib/matplotlib/issues/2654
        return fig, ax
