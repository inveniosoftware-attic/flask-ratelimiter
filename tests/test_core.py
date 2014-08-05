# -*- coding: utf-8 -*-
##
## This file is part of Flask-RateLimiter
## Copyright (C) 2014 CERN.
##
## Flask-RateLimiter is free software; you can redistribute it and/or
## modify it under the terms of the Revised BSD License; see LICENSE
## file for more details.

from __future__ import absolute_import

import six
from .helpers import FlaskTestCase, skipUnless

from flask import request, g
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
            self.assertEqual(request.endpoint, 'test_limit')
            self.assertEqual(g._rate_limit_info.limit, 2)
            self.assertEqual(g._rate_limit_info.remaining, 1)
            self.assertEqual(g._rate_limit_info.limit_exceeded, False)
            self.assertEqual(g._rate_limit_info.per, 10)
            self.assertEqual(g._rate_limit_info.send_x_headers, True)
            self.assertEqual(res.status_code, 200)

            res = c.get('/limit')
            self.assertEqual(g._rate_limit_info.limit, 2)
            self.assertEqual(g._rate_limit_info.remaining, 0)
            self.assertEqual(g._rate_limit_info.limit_exceeded, True)
            self.assertEqual(g._rate_limit_info.per, 10)
            self.assertEqual(g._rate_limit_info.send_x_headers, True)
            self.assertIn(six.b('Rate limit was exceeded'), res.data)
            self.assertEqual(res.status_code, 429)

            res = c.get('/limit')
            self.assertEqual(g._rate_limit_info.limit, 2)
            self.assertEqual(g._rate_limit_info.remaining, 0)
            self.assertEqual(g._rate_limit_info.limit_exceeded, True)
            self.assertEqual(res.status_code, 429)

    @skipUnless(is_cache_installed, 'Flask-Cache is not installed')
    def test_flask_cache_prefix(self):
        cache = Cache(self.app, config={'CACHE_TYPE': 'redis'})
        prefix = 'flask_cache_prefix'

        self.app.config.setdefault('CACHE_KEY_PREFIX', prefix)
        self.app.config.setdefault('RATELIMITER_BACKEND', 'FlaskCacheRedisBackend')
        self.app.config.setdefault('RATELIMITER_BACKEND_OPTIONS',
                                   {'cache': cache})
        r = RateLimiter(self.app)
        self.assertEqual(self.app.config['RATELIMITER_KEY_PREFIX'], prefix)

    def test_ratelimit_headers(self):
        rl = RateLimiter(self.app)

        @self.app.route('/limit3')
        @ratelimit(2, 10)
        def test_limit3():
            return 'limit'

        with self.app.test_client() as c:
            res = c.get('/limit3')
            self.assertEqual(request.endpoint, 'test_limit3')
            self.assertEqual(int(res.headers.get('X-RateLimit-Limit')), 2)
            self.assertEqual(int(res.headers.get('X-RateLimit-Remaining')), 1)
            self.assertIsNot(res.headers.get('X-RateLimit-Reset', None), None)

    def test_ratelimit_no_headers_sent(self):
        self.app.config.setdefault('RATELIMITER_INJECT_X_HEADERS', False)
        rl = RateLimiter(self.app)

        @self.app.route('/limit4')
        @ratelimit(2, 10)
        def test_limit4():
            return 'limit'

        with self.app.test_client() as c:
            res = c.get('/limit4')
            self.assertEqual(request.endpoint, 'test_limit4')
            self.assertEqual(res.headers.get('X-RateLimit-Limit', None), None)
            self.assertEqual(res.headers.get('X-RateLimit-Remaining', None), None)


class TestGetBackend(FlaskTestCase):
    """
    Tests get_backend function.
    """

    def test_get_correct_backend(self):
        """
        tests get_backend function with correct input
        """
        backend = RateLimiter.get_backend('SimpleRedisBackend')
        self.assertEqual(backend.__name__, 'SimpleRedisBackend')

    def test_get_incorrect_backend(self):
        """
        tests get_backend function with incorrect input
        """
        self.assertEqual(RateLimiter.get_backend('CrazyBackendX').__name__, 'SimpleRedisBackend')
