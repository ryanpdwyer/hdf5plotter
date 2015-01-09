# -*- coding: utf-8 -*-
"""A simple command line interface, with the command h5plot.

The command should look something like this:

h5plot myfile.h5 --x-data=x --y-data=y --scale=linear\
    --x-min=1 --x-max=10 --y-min=1 --y-max=10 --output=fig1.png

h5plot myfile.h5
"""

import click
import pandas as pd
from hdf5plotter import PlotFromManyFiles
from hdf5plotter._csvplot import plot_csv, get_csv_axes, rescale_column


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
        fig.show()
    return 0


@click.command()
@click.argument('inputs', type=click.Path(exists=True), nargs=-1)
@click.option('--output', '-o', type=str, default=None, help='output file')
@click.option('--x-data', '-x', type=str, default=None, help='x dataset')
@click.option('--y-data', '-y', type=str, default=None, help='y dataset')
@click.option('--scale', '-s', type=str, default='linear', help='plot scale: linear semilogx semilogy loglog')
@click.option('--xlim', '-xl', nargs=2, type=float, help='x limits min max')
@click.option('--ylim', '-yl', nargs=2, type=float, help='y limits min max')
def csvplot(inputs, output, x_data, y_data, scale, xlim, ylim):
    if xlim == tuple():
        xlim = None
    if ylim == tuple():
        ylim = None

    x = []
    y = []

    for filename in inputs:
        new_x, new_y = get_csv_axes(filename, x, y)
        x.append(new_x)
        y.append(new_y)

    plot_csv(x, y, scale=scale, xlim=xlim, ylim=ylim)
    
    fig.tight_layout()

    if output is None:
        fig.show()
    else:
        fig.savefig(output)

    return 0


@click.command()
@click.argument('fname', type=click.Path(exists=True))
@click.option('--output', '-o', default=None, type=click.Path())
@click.option('--column', '-c', type=str, prompt=True, nargs=2,
              help="column new_unit", multiple=True)
@click.option('--separator', '-s', default=',', type=str)
def csvscale(fname, output, column, separator):
    df = pd.read_csv(fname, sep=separator, encoding='utf-8')
    
    for col, new_unit in column:
        df = rescale_column(df, col, new_unit)

    if output is None:
        output = fname
    df.to_csv(output, sep=separator, index=False, encoding='utf-8')
    