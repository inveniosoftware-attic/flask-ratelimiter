# -*- coding: utf-8 -*-
#
# This file is part of Flask-RateLimiter
# Copyright (C) 2014, 2015 CERN.
#
# Flask-RateLimiter is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Test rate limiter backends."""

from __future__ import absolute_import

from os import environ

from flask.ext.cache import Cache
from flask.ext.ratelimiter import RateLimiter
from flask.ext.ratelimiter.backends import Backend, FlaskCacheRedisBackend, \
    SimpleRedisBackend

import redis

from .helpers import FlaskTestCase


class TestAbstractBackend(FlaskTestCase):

    """Test rate limiter abstract backend."""

    def test_backend(self):
        """Test rate limiter backend parameter setting and updating."""
        b = Backend(key1='key1', key2='key2')
        self.assertEqual(b.key1, 'key1')
        self.assertRaises(NotImplementedError, b.update)


class TestSimpleRedisBackend(FlaskTestCase):

    """Test rate limiter simple Redis backend."""

    def setUp(self):
        """Set up for tests."""
        self.redis = redis.StrictRedis(host=environ.get('REDIS_HOST',
                                                        'localhost'))
        self.redis.flushdb()
        super(TestSimpleRedisBackend, self).setUp()

    def test_backend(self):
        """Test simple redis backend."""
        b = SimpleRedisBackend(host=environ.get('REDIS_HOST', 'localhost'))
        self.assertIsNot(b.cache, None)

        limit_exceeded, remaining, reset = b.update('redis_backend', 3, 5)
        self.assertEqual(limit_exceeded, False)
        self.assertEqual(remaining, 2)

        limit_exceeded, remaining, reset = b.update('redis_backend', 3, 5)
        self.assertEqual(limit_exceeded, False)
        self.assertEqual(remaining, 1)

        limit_exceeded, remaining, reset = b.update('redis_backend', 3, 5)
        self.assertEqual(limit_exceeded, False)
        self.assertEqual(remaining, 0)

        limit_exceeded, remaining, reset = b.update('redis_backend', 3, 5)
        self.assertEqual(limit_exceeded, True)
        self.assertEqual(remaining, 0)

        # Assert that we don't increase past 3 despite there being 4 requests
        keys = self.redis.keys()
        self.assertEqual(len(keys), 1)
        self.assertEqual(self.redis.get(keys[0]).decode('utf-8'), '3')


class TestFlaskCacheRedisBackend(FlaskTestCase):

    """Test rate limiter Flask-Cache Redis backend."""

    def setUp(self):
        """Set up for tests."""
        redis.StrictRedis(host=environ.get('REDIS_HOST',
                                           'localhost')).flushdb()
        super(TestFlaskCacheRedisBackend, self).setUp()

    def test_backend_with_app(self):
        """Test simple redis backend with app."""
        cache = Cache(self.app, config={'CACHE_TYPE': 'redis',
                                        'CACHE_REDIS_HOST': environ.get(
                                            'REDIS_HOST', 'localhost')})

        self.app.config.setdefault('RATELIMITER_BACKEND',
                                   'FlaskCacheRedisBackend')
        self.app.config.setdefault('RATELIMITER_BACKEND_OPTIONS',
                                   {'cache': cache,
                                    'host': environ.get('REDIS_HOST',
                                                        'localhost')})
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
        self.assertEqual(limit_exceeded, False)
        self.assertEqual(remaining, 0)

        limit_exceeded, remaining, reset = r.backend.update(
            'flask_cache_backend', 3, 5)
        self.assertEqual(limit_exceeded, True)
        self.assertEqual(remaining, 0)

    def test_backend_wrong_cache(self):
        """Test rate limiter Flask-Cache Redis backend with wrong cache."""
        self.assertRaises(ValueError,
                          lambda: FlaskCacheRedisBackend('WrongCache'))
