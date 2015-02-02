# -*- coding: utf-8 -*-
"""
Command line interfaces
=======================

A simple command line interface, with the command h5plot.

The command should look something like this::

    h5plot myfile.h5 --x-data=x --y-data=y --scale=linear\
    --x-min=1 --x-max=10 --y-min=1 --y-max=10 --output=fig1.png

    h5plot myfile.h5


csvplot
-------

.. image:: images/ex.png

Here is an example image made with ``csvplot``.
"""

import time
import tempfile
import webbrowser

import pathlib
import click
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from hdf5plotter import PlotFromManyFiles
from hdf5plotter._csvplot import plot_csv, get_csv_axes, rescale_column


def show_file(path):
    uri = str(pathlib.Path(path).absolute().as_uri())
    webbrowser.open(uri)




@click.command()
@click.argument('inputs', type=click.Path(exists=True), nargs=-1)
@click.option('--output', '-o', type=str, default=None, help='output file')
@click.option('--x-data', '-x', type=str, default='x', help='x dataset')
@click.option('--y-data', '-y', type=str, default='y', help='y dataset')
@click.option('--scale', '-s', type=str, default='linear', help='plot scale: linear semilogx semilogy loglog')
@click.option('--xlim', '-xl', nargs=2, type=float, help='x limits min max')
@click.option('--ylim', '-yl', nargs=2, type=float, help='y limits min max')
@click.option('--seaborn/--no-seaborn', default=False, help='Use seaborn plot style')
def cli(inputs, output, x_data, y_data, scale, xlim, ylim, seaborn):
    if xlim == tuple():
        xlim = None
    if ylim == tuple():
        ylim = None

    if seaborn:
        import seaborn

    p = PlotFromManyFiles()

    for fname in inputs:
        p.add(fname)

    fig, ax = p.plot(x=x_data, y=y_data,
                     scale=scale,
                     xlim=xlim, ylim=ylim,
                     filename=output)

    if output is None:
        with tempfile.NamedTemporaryFile(suffix='.pdf') as f:
            fig.savefig(f, format='pdf')
            uri = pathlib.Path(f.name).absolute().as_uri()
            webbrowser.open(uri)
            time.sleep(5)
    else:
        fig.savefig(output)

    return 0


@click.command()
@click.argument('inputs', type=click.Path(exists=True), nargs=-1)
@click.option('--output', '-o', type=str, default=None, help='output file')
@click.option('--x-data', '-x', type=str, default=None, help='x dataset')
@click.option('--y-data', '-y', type=str, default=None, help='y dataset')
@click.option('--scale', '-s', type=str, default='linear', help='plot scale: linear semilogx semilogy loglog')
@click.option('--xlim', '-xl', nargs=2, type=float, help='x limits min max')
@click.option('--ylim', '-yl', nargs=2, type=float, help='y limits min max')
@click.option('--format-output', '-f', type=str, default=None, help='output format')
@click.option('--seaborn/--no-seaborn', default=False, help='Use seaborn plot style')
@click.option('--text-size', '-ts', default=16, type=float)
@click.option('--line-width', '-lw', default=2.5, type=float)
@click.option('--fig-size', '-fs', default=(8, 6), nargs=2, type=float)
@click.option('--show/--no-show', default=True)
def csvplot(inputs, output, x_data, y_data, scale, xlim, ylim, format_output,
            seaborn, text_size, line_width, fig_size, show):
    if xlim == tuple():
        xlim = None
    if ylim == tuple():
        ylim = None

    x = []
    y = []

    for filename in inputs:
        new_x, new_y = get_csv_axes(filename, x_data, y_data)
        x.append(new_x)
        y.append(new_y)

    if seaborn:
        import seaborn

    rcParams = {'lines.linewidth': line_width,
                'font.size': text_size,
                'figure.figsize': fig_size}

    fig, ax = plot_csv(x, y, scale=scale, xlim=xlim, ylim=ylim,
                       rcParams=rcParams)

    fig.tight_layout()

    if output is None and format_output is None:
        with tempfile.NamedTemporaryFile(suffix='.pdf') as f:
            fig.savefig(f, format='pdf')
            uri = str(pathlib.Path(f.name).absolute().as_uri())
            webbrowser.open(uri)
            time.sleep(5)

        return 0

    if output is None and len(inputs) == 1:
        input_name = pathlib.Path(inputs[0])
        output = str(input_name.with_suffix('.'+format_output))
    elif output is None and len(inputs) > 1:
        raise ValueError(
            "If plotting from multiple files, must provide output filename")

    fig.savefig(output)

    if show:
        uri = str(pathlib.Path(output).absolute().as_uri())
        webbrowser.open(uri)

    return 0


@click.command()
@click.argument('fname', type=click.Path(exists=True))
@click.option('--output', '-o', default=None, type=click.Path())
@click.option('--column', '-c', type=str, prompt=True, nargs=2,
              help="column new_unit", multiple=True)
def csvscale(fname, output, column):
    df = pd.read_csv(fname, encoding='utf-8')

    for col, new_unit in column:
        df = rescale_column(df, col, new_unit)

    if output is None:
        print(df.head())
        choice = raw_input("Overwrite file? [y/N]\n").lower()
        if choice[0] != 'y':
            raise ValueError("Stopping.")

        output = fname

    df.to_csv(output, index=False, encoding='utf-8')
