# -*- coding: utf-8 -*-
from __future__ import absolute_import


def concatenate_path_pk(path, *args):
    """
    Receive path and args and concatenate to create the path needed
    for an object query.

    Make sure parameters are plugged in in the right order. It must
    be aligned with the Bexio API, so the endpoints are valid. Check
    out the official docs to see, how the final path should look like.

    :param: str, endpoint path to be used (must be first arg)
    :param: list, *args that come after
    :return: str, concatenated path
    """
    return '/'.join([str(path)] + [str(arg) for arg in args])
