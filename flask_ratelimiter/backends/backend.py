# -*- coding: utf-8 -*-
#
# This file is part of Flask-RateLimiter
# Copyright (C) 2014 CERN.
#
# Flask-RateLimiter is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

from six import iteritems


class Backend(object):
    """
    Abstract backend for inheriting purposes.
    """

    def __init__(self, **kwargs):

        for key, value in iteritems(kwargs):
            setattr(self, key, value)

    def update(self):
        """
        Every new backend needs to implement this function.

        Function needs to return tuple with two values:
        * limit_exceeded - boolean, checks if limit was exceeded
        * remaining - how many request have left to exceed the limit
        * reset - the remaining window before the rate limit resets
        """
        raise NotImplementedError
