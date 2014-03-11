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
