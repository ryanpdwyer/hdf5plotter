# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from hdf5plotter import u
from hdf5plotter._plot import plot
from hdf5plotter._util import replace_unit_label_ascii
import re




def get_unit(string):
    """Return a unit string if it exists"""
    unit = re.findall(r"(\[.*\]|\(.*\))", string)
    if unit == []:
        return ''
    else:
        return re.findall(r"\[.*\]", string)[0][1:-1]


def axis(series):
    ax = series.copy()
    ax.unit = u(get_unit(ax.name))
    ax.label = ax.name[:ax.name.find('[')]
    return ax

def get_csv_axes(filename, x=None, y=None):
    df = pd.read_csv(filename)

    if x is None:
        x_data = axis(df.iloc[:, 0])
    else:
        x_data = axis(df.filter(like=x))
    if y is None:
        y_data = axis(df.iloc[:, 1])
    else:
        y_data = axis(df.filter(like=y))

    return x_data, y_data


def get_default_plot_label(series):
    return replace_unit_label(series.name, series.unit)


def plot_csv(x, y, scale='linear', xlim=None, ylim=None,
             xlabel=None, ylabel=None):
    if xlabel is None:
        if nested_iterable(x):
            xlabel = replace_unit_label(x[0].name, x[0].unit)
        else:
            xlabel = replace_unit_label(x.name, x.unit)

    if ylabel is None:
        if nested_iterable(y):
            ylabel = y[0].name
        else:
            ylabel = y.name

    return plot(np.array(x), np.array(y), scale=scale,
        xlim=xlim, ylim=ylim, xlabel=xlabel, ylabel=ylabel)


def column(df, string):
    """Find columns containing string"""
    return tuple(col for col in df.columns if string in col)

def get_column(df, string):
    try:
        return df[column(df, string)[0]]
    except KeyError:
        raise KeyError("{0} matches multiple columns in df\n{1}".format(
            string, df.columns))

def rescale(col, new_unit):
    unit = u(unicode(get_unit(col.name)))
    scale_factor = 1.0/unit.to(new_unit).magnitude
    new_name = replace_unit_label_ascii(col.name, new_unit)
    return pd.Series(col * scale_factor, name=new_name)

def rescale_column(df, string, new_unit):
    # Somehow I am creating a new
    col = get_column(df, string)
    new_col = rescale(col, new_unit)
    new_df = df.copy()
    new_df[col.name] = new_col
    new_df.rename(columns={col.name: new_col.name}, inplace=True)
    return new_df
