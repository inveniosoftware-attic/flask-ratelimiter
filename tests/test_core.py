# -*- coding: utf-8 -*-
#
# This file is part of Flask-RateLimiter
# Copyright (C) 2014 CERN.
#
# Flask-RateLimiter is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Test core rate limiter funcionality."""

from __future__ import absolute_import

from os import environ

from flask import g, request
from flask.ext.ratelimiter import RateLimiter, ratelimit

import six

from .helpers import FlaskTestCase, skipUnless

try:
    from flask.ext.cache import Cache
    is_cache_installed = True
except ImportError:
    is_cache_installed = False


class TestRateLimiter(FlaskTestCase):

    """Test rate limiting functionality."""

    def test_rate_limiting_simple_redis_backend(self):
        """Test rate limiter with simple Redis backend."""
        self.app.config.setdefault('RATELIMITER_BACKEND_OPTIONS',
                                   {'host': environ.get('REDIS_HOST',
                                                        'localhost')})
        RateLimiter(self.app)

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

    def test_dynamic_ratelimit(self):
        """Test that passing callable limit to @ratelimit behaves correctly"""
        self.app.config.setdefault('RATELIMITER_BACKEND_OPTIONS',
                                   {'host': environ.get('REDIS_HOST',
                                                        'localhost')})
        RateLimiter(self.app)

        def dynamic_limit(default, **kwargs):
            """
            A function that returns a rate limit based on some incoming
            information
            The function may be passed key_func() and scope_func() as kwargs to
            help to do that, but in this test we directly use the http header
            to test functionality
            """
            self.assertIn('key', kwargs)
            self.assertIn('scope', kwargs)
            factor = request.headers.get('multiply_ratelimit')
            if factor is None:
                return default
            return default * int(factor)

        @self.app.route('/dynamic-limit')
        @ratelimit(lambda **kwargs: dynamic_limit(default=2, **kwargs), 10)
        def test_dynamic_limit():
            return 'limit'

        with self.app.test_client() as c:
            res = c.get('/dynamic-limit')
            self.assertEqual(g._rate_limit_info.limit, 2)
            self.assertEqual(g._rate_limit_info.remaining, 1)
            self.assertEqual(g._rate_limit_info.limit_exceeded, False)
            self.assertEqual(g._rate_limit_info.per, 10)
            self.assertEqual(g._rate_limit_info.send_x_headers, True)
            self.assertEqual(res.status_code, 200)

            res = c.get('/dynamic-limit', headers={'multiply_ratelimit': 10})
            self.assertEqual(g._rate_limit_info.limit, 20)
            self.assertEqual(g._rate_limit_info.remaining, 18)
            self.assertEqual(g._rate_limit_info.limit_exceeded, False)
            self.assertEqual(g._rate_limit_info.per, 10)
            self.assertEqual(g._rate_limit_info.send_x_headers, True)
            self.assertEqual(res.status_code, 200)


    @skipUnless(is_cache_installed, 'Flask-Cache is not installed')
    def test_flask_cache_prefix(self):
        """Test rate limiter with Flask-Cache Redis backend."""
        cache = Cache(self.app, config={'CACHE_TYPE': 'redis'})
        prefix = 'flask_cache_prefix'

        self.app.config.setdefault('CACHE_KEY_PREFIX', prefix)
        self.app.config.setdefault('RATELIMITER_BACKEND',
                                   'FlaskCacheRedisBackend')
        self.app.config.setdefault('RATELIMITER_BACKEND_OPTIONS',
                                   {'cache': cache})
        RateLimiter(self.app)
        self.assertEqual(self.app.config['RATELIMITER_KEY_PREFIX'], prefix)

    def test_ratelimit_headers(self):
        """Test rate limiter backend options."""
        self.app.config.setdefault('RATELIMITER_BACKEND_OPTIONS',
                                   {'host': environ.get('REDIS_HOST',
                                                        'localhost')})
        RateLimiter(self.app)

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
        """Test rate limiter header sending."""
        self.app.config.setdefault('RATELIMITER_INJECT_X_HEADERS', False)
        self.app.config.setdefault('RATELIMITER_BACKEND_OPTIONS',
                                   {'host': environ.get('REDIS_HOST',
                                                        'localhost')})
        RateLimiter(self.app)

        @self.app.route('/limit4')
        @ratelimit(2, 10)
        def test_limit4():
            return 'limit'

        with self.app.test_client() as c:
            res = c.get('/limit4')
            self.assertEqual(request.endpoint, 'test_limit4')
            self.assertEqual(res.headers.get('X-RateLimit-Limit', None),
                             None)
            self.assertEqual(res.headers.get('X-RateLimit-Remaining', None),
                             None)


class TestGetBackend(FlaskTestCase):

    """Test get_backend functionality."""

    def test_get_correct_backend(self):
        """Test get_backend function with correct input."""
        backend = RateLimiter.get_backend('SimpleRedisBackend')
        self.assertEqual(backend.__name__, 'SimpleRedisBackend')

    def test_get_incorrect_backend(self):
        """Test get_backend function with incorrect input."""
        self.assertEqual(RateLimiter.get_backend('CrazyBackendX').__name__,
                         'SimpleRedisBackend')
