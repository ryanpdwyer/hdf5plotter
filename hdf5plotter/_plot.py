import numpy as np
import collections
import matplotlib as mpl
import matplotlib.pyplot as plt

"""Expectation:
plot(x=[1, 2, 3], y=[1, 4, 9])
plot(x=[[1, 2, 3], [1, 1.5, 2, 2.5, 3]], y=[[1, 4, 9], [1, 2, 4, 6, 9]])

"""


def iterable(x):
    """True if x is an iterable other than a string: some sort of list-like
    container"""
    if isinstance(x, str):
        return False
    else:
        return isinstance(x, collections.Iterable)


def nested_iterable(x):
    """Return true if x is (at least) list of lists, or a 2D numpy array, or
    list of 1D numpy arrays.

    Raises a TypeError if passed a non-iterable."""
    return all(iterable(i) for i in x)


def plot(x, y, magic=None, scale='linear', xlabel=None, ylabel=None, shape=None,
         xlim=None, ylim=None, rcParams={}):
    """A all in one plotting function which adds scale, labels, limits, shape,
    and the option to specify additional parameters."""
    with mpl.rc_context(rc=rcParams):
        fig, ax = plt.subplots()

        plotting_functions = {
            'linear': ax.plot,
            'semilogy': ax.semilogy,
            'semilogx': ax.semilogx,
            'loglog': ax.loglog}

        plot_scale_func = plotting_functions[scale]

        def plot_single(plot_func, x, y, magic):
            if magic is None:
                return plot_func(x, y)
            else:
                return plot_func(x, y, magic)


        nested_x = nested_iterable(x)
        nested_y = nested_iterable(y)
        iterable_magic = iterable(magic)

        if nested_x and nested_x:
            for xi, yi in zip(x, y):
                plot_scale_func(xi, yi)
        elif nested_y:
            for yi in y:
                plot_scale_func(x, yi)
        elif nested_x:
            raise ValueError("Give multiple y arrays for multiple x arrays")
        else:
            plot_scale_func(x, y)

        if xlabel is not None:
            ax.set_xlabel(xlabel)
        if ylabel is not None:
            ax.set_ylabel(ylabel)

        if xlim is not None:
            ax.set_xlim(xlim)
        if ylim is not None:
            ax.set_ylim(ylim)

        fig.tight_layout()
        return fig, ax
