# -*- coding: utf-8 -*-
"""A simple command line interface, with the command h5plot.

The command should look something like this:

h5plot myfile.h5 --x-data=x --y-data=y --scale=linear\
    --x-min=1 --x-max=10 --y-min=1 --y-max=10 --output=fig1.png

h5plot myfile.h5
"""

import click
from hdf5plotter import PlotFromManyFiles

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
