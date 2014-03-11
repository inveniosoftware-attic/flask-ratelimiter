# -*- coding: utf-8 -*-
##
## This file is part of Flask-RateLimiter
## Copyright (C) 2014 CERN.
##
## Flask-RateLimiter is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Flask-RateLimiter is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Flask-RateLimiter; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
##
## In applying this licence, CERN does not waive the privileges and immunities
## granted to it by virtue of its status as an Intergovernmental Organization
## or submit itself to any jurisdiction.

from __future__ import absolute_import

from .simpleredis_backend import SimpleRedisBackend


class FlaskCacheRedisBackend(SimpleRedisBackend):
    """
    Backend which uses Flask-Cache to store keys in Redis.
    """
    expiration_window = 10

    def __init__(self, cache=None, **kwargs):
        self.cache = cache
        if self.cache.__class__.__name__ != 'Cache':
            raise ValueError('Incorrect cache was passed as an argument')
        self.pipeline = self.cache.cache._client.pipeline()
        super(SimpleRedisBackend, self).__init__(**kwargs)