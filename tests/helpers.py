# -*- coding: utf-8 -*-
#
# This file is part of Flask-RateLimiter
# Copyright (C) 2014 CERN.
#
# Flask-RateLimiter is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

import sys

if sys.version_info < (2, 7):
    import functools
    import nose
    from unittest2 import TestCase

    def skipUnless(condition, msg):
        def decorated(test):
            @functools.wraps(test)
            def decorator(*args, **kwargs):
                if condition:
                    return test(*args, **kwargs)
                raise nose.SkipTest(msg)
            return decorator
        return decorated

else:
    from unittest import TestCase, skipUnless

from flask import Flask


class FlaskTestCase(TestCase):
    """
    Mix-in class for creating the Flask application
    """

    def setUp(self):
        app = Flask(__name__)
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.logger.disabled = True
        self.app = app

__all__ = ['FlaskTestCase', 'skipUnless']
