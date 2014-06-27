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

import unittest
from .helpers import FlaskTestCase, skipUnless
from flask.ext.ratelimiter import RateLimiter
from flask.ext.ratelimiter.backends import *
from flask.ext.cache import Cache

class TestAbstractBackend(FlaskTestCase):

    def test_backend(self):
        b = Backend(key1='key1', key2='key2')
        self.assertEqual(b.key1, 'key1')
        self.assertRaises(NotImplementedError, b.update)


class TestSimpleRedisBackend(FlaskTestCase):

    def test_backend(self):
        b = SimpleRedisBackend()
        self.assertIsNot(b.redis, None)
        self.assertEqual(b.pipeline.__class__.__name__, 'Pipeline')

        limit_exceeded, remaining, reset = b.update('redis_backend', 3, 5)
        self.assertEqual(limit_exceeded, False)
        self.assertEqual(remaining, 2)

        limit_exceeded, remaining, reset = b.update('redis_backend', 3, 5)
        self.assertEqual(limit_exceeded, False)
        self.assertEqual(remaining, 1)

        limit_exceeded, remaining, reset = b.update('redis_backend', 3, 5)
        self.assertEqual(limit_exceeded, True)
        self.assertEqual(remaining, 0)


class TestFlaskCacheRedisBackend(FlaskTestCase):

    def test_backend_with_app(self):
        cache = Cache(self.app, config={'CACHE_TYPE': 'redis'})

        self.app.config.setdefault('RATELIMITER_BACKEND',
                                   'FlaskCacheRedisBackend')
        self.app.config.setdefault('RATELIMITER_BACKEND_OPTIONS',
                                   {'cache': cache})
        r = RateLimiter(self.app)

        limit_exceeded, remaining, reset = r.backend.update(
            'flask_cache_backend', 3, 5)
        self.assertEqual(limit_exceeded, False)
        self.assertEqual(remaining, 2)

        limit_exceeded, remaining, reset = r.backend.update(
            'flask_cache_backend', 3, 5)
        self.assertEqual(limit_exceeded, False)
        self.assertEqual(remaining, 1)

        limit_exceeded, remaining, reset = r.backend.update(
            'flask_cache_backend', 3, 5)
        self.assertEqual(limit_exceeded, True)
        self.assertEqual(remaining, 0)

    def test_backend_wrong_cache(self):
        self.assertRaises(ValueError,
                          lambda: FlaskCacheRedisBackend('WrongCache'))
