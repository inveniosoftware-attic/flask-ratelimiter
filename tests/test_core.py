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
from .helpers import FlaskTestCase

from flask import Blueprint, Flask, request, url_for, g, current_app
from flask.ext.ratelimiter import RateLimiter, \
    ratelimit
try:
    from flask.ext.cache import Cache
    is_cache_installed = True
except ImportError:
    is_cache_installed = False



class TestRateLimiter(FlaskTestCase):
    """
    Tests of rate limiting.
    """
    def test_rate_limiting_simple_redis_backend(self):
        rl = RateLimiter(self.app)

        @self.app.route('/limit')
        @ratelimit(2, 10)
        def test_limit():
            return 'limit'

        with self.app.test_client() as c:
            res = c.get('/limit')
            assert request.endpoint == 'test_limit'
            assert g._rate_limit_info.limit == 2
            assert g._rate_limit_info.remaining == 1
            assert g._rate_limit_info.limit_exceeded == False
            assert g._rate_limit_info.per == 10
            assert g._rate_limit_info.send_x_headers == True
            assert res.status_code == 200

            res = c.get('/limit')
            assert g._rate_limit_info.limit == 2
            assert g._rate_limit_info.remaining == 0
            assert g._rate_limit_info.limit_exceeded == True
            assert g._rate_limit_info.per == 10
            assert g._rate_limit_info.send_x_headers == True
            assert res.get_data() == 'Rate limit was exceeded'
            assert res.status_code == 429

            res = c.get('/limit')
            assert g._rate_limit_info.limit == 2
            assert g._rate_limit_info.remaining == 0
            assert g._rate_limit_info.limit_exceeded == True
            assert res.status_code == 429

    @unittest.skipUnless(is_cache_installed, 'Flask-Cache is not installed')
    def test_flask_cache_prefix(self):
        cache = Cache(self.app, config={'CACHE_TYPE': 'redis'})
        prefix = 'flask_cache_prefix'

        self.app.config.setdefault('CACHE_KEY_PREFIX', prefix)
        self.app.config.setdefault('RATELIMITER_BACKEND', 'FlaskCacheRedisBackend')
        self.app.config.setdefault('RATELIMITER_BACKEND_OPTIONS',
                                   {'cache': cache})
        r = RateLimiter(self.app)
        assert self.app.config['RATELIMITER_KEY_PREFIX'] == prefix

    def test_ratelimit_headers(self):
        rl = RateLimiter(self.app)

        @self.app.route('/limit3')
        @ratelimit(2, 10)
        def test_limit3():
            return 'limit'

        with self.app.test_client() as c:
            res = c.get('/limit3')
            assert request.endpoint == 'test_limit3'
            assert int(res.headers.get('X-RateLimit-Limit')) == 2
            assert int(res.headers.get('X-RateLimit-Remaining')) == 1
            assert res.headers.get('X-RateLimit-Reset', None) != None

    def test_ratelimit_no_headers_sent(self):
        self.app.config.setdefault('RATELIMITER_INJECT_X_HEADERS', False)
        rl = RateLimiter(self.app)

        @self.app.route('/limit4')
        @ratelimit(2, 10)
        def test_limit4():
            return 'limit'

        with self.app.test_client() as c:
            res = c.get('/limit4')
            assert request.endpoint == 'test_limit4'
            assert res.headers.get('X-RateLimit-Limit', None) == None
            assert res.headers.get('X-RateLimit-Remaining', None) == None


class TestGetBackend(FlaskTestCase):
    """
    Tests get_backend function.
    """

    def test_get_correct_backend(self):
        """
        tests get_backend function with correct input
        """
        backend = RateLimiter.get_backend('SimpleRedisBackend')
        assert backend.__name__ == 'SimpleRedisBackend'

    def test_get_incorrect_backend(self):
        """
        tests get_backend function with incorrect input
        """
        assert RateLimiter.get_backend('CrazyBackendX').__name__ == 'SimpleRedisBackend'