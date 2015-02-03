# -*- coding: utf-8 -*-
"""
=======
csvutil
=======

Utilities for working with csv data, including dealing with metadata using
INI configuration in comments.

"""
from __future__ import division, print_function, absolute_import

import io
import StringIO
import ConfigParser
from collections import OrderedDict
import pandas as pd
from pandas.io.common import get_filepath_or_buffer

def ini_config_to_ordered_dict(ini_config):
    od = OrderedDict()
    for section in ini_config.sections():
        od[section] = OrderedDict(ini_config.items(section))

    return od

def parse_csv(filepath_or_buffer, comment="#"):
    if isinstance(filepath_or_buffer, str) or isinstance(filepath_or_buffer, unicode):
        f = io.open(filepath_or_buffer, 'r', encoding='utf-8')
        close = True
    else:
        f = filepath_or_buffer
        close = False

    ini_lines = [line[1:] for line in f.readlines() if line.startswith(comment)]
    ini_string_io = StringIO.StringIO("\n".join(ini_lines))
    c = ConfigParser.ConfigParser()
    c.readfp(ini_string_io)

    od = ini_config_to_ordered_dict(c)

    f.seek(0)

    df = pd.read_csv(filepath_or_buffer, comment=comment, engine='python')
    
    if close:
        f.close()
    
    df.metadata = od

    return df
