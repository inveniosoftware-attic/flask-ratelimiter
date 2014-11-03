# -*- coding: utf-8 -*-
#
# This file is part of Flask-RateLimiter
# Copyright (C) 2014 CERN.
#
# Flask-RateLimiter is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Implement Flask-Cache backend."""

from __future__ import absolute_import

from .simpleredis_backend import SimpleRedisBackend


class FlaskCacheRedisBackend(SimpleRedisBackend):

    """Flask-Cache backend that stores keys in Redis."""

    expiration_window = 10

    def __init__(self, cache=None, **kwargs):
        """Store Flask-Cache instance."""
        self.cache = cache
        if self.cache.__class__.__name__ != 'Cache':
            raise ValueError('Incorrect cache was passed as an argument')
        self.pipeline = self.cache.cache._client.pipeline()
        super(SimpleRedisBackend, self).__init__(**kwargs)
