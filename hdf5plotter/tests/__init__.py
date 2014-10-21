# -*- coding: utf-8 -*-
import os
import errno


def silentremove(filename):
    """If ``filename`` exists, delete it. Otherwise, return nothing.
       See http://stackoverflow.com/q/10840533/2823213."""
    try:
        os.remove(filename)
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occured