# -*- coding: utf-8 -*-
#
# This file is part of Flask-RateLimiter
# Copyright (C) 2014 CERN.
#
# Flask-RateLimiter is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Implement Redis backend."""

from __future__ import absolute_import

import time
from redis import Redis

from .backend import Backend


class SimpleRedisBackend(Backend):

    """Simple redis backend.

    Directly connects to Redis and uses its pipeline
    to store keys in database.
    """

    expiration_window = 10

    def __init__(self, cache=None, **kwargs):
        """Create Redis connetion instance."""
        super(SimpleRedisBackend, self).__init__(**kwargs)
        if cache is None:
            cache = Redis(**kwargs)
        self.cache = cache

    def update(self, key_prefix, limit, per):
        """Update database for specific key_prefix.

        Key prefix is basically an info about endpoint and
        user requesting specific endpoint, for example:

        .. code-block:: text

            'rate_limit/127.0.0.1/index_view'

        :param key_prefix: prefix for the key we want to store in redis
        :param limit: max number of request per some time
        :param per: time in seconds during which we count records
        """
        reset = (int(time.time()) // per) * per + per
        key = key_prefix + str(reset)

        current = self.cache.get(key)
        if current is not None:
            current = min(int(current), limit)

        limit_exceeded = True
        if current is None or current < limit:
            limit_exceeded = False
            pipeline = self.cache.pipeline()
            pipeline.incr(key)
            pipeline.expireat(key, reset + self.expiration_window)
            current = min(pipeline.execute()[0], limit)

        remaining = limit - current
        return limit_exceeded, remaining, reset
