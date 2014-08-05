# -*- coding: utf-8 -*-
##
## This file is part of Flask-RateLimiter
## Copyright (C) 2014 CERN.
##
## Flask-RateLimiter is free software; you can redistribute it and/or
## modify it under the terms of the Revised BSD License; see LICENSE
## file for more details.

from __future__ import absolute_import

from .helpers import FlaskTestCase
from flask_ratelimiter import RateLimiter


class TestRateLimiter(FlaskTestCase):
    """
    Tests of extension creation
    """
    def test_version(self):
        # Assert that version number can be parsed.
        from flask_ratelimiter import __version__
        from distutils.version import LooseVersion
        LooseVersion(__version__)

    def test_creation(self):
        assert 'ratelimiter' not in self.app.extensions
        RateLimiter(app=self.app)
        assert isinstance(self.app.extensions['ratelimiter'], RateLimiter)

    def test_creation_old_flask(self):
        # Simulate old Flask (pre 0.9)
        del self.app.extensions
        RateLimiter(app=self.app)
        assert isinstance(self.app.extensions['ratelimiter'], RateLimiter)

    def test_creation_init(self):
        assert 'ratelimiter' not in self.app.extensions
        r = RateLimiter()
        r.init_app(app=self.app)
        assert isinstance(self.app.extensions['ratelimiter'], RateLimiter)

    def test_double_creation(self):
        RateLimiter(app=self.app)
        self.assertRaises(RuntimeError, RateLimiter, app=self.app)
