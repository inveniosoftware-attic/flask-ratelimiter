# -*- coding: utf-8 -*-
#
# This file is part of Flask-RateLimiter
# Copyright (C) 2015 CERN.
#
# Flask-RateLimiter is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""A simple demo application showing Flask-RateLimiter in action.

Usage:
  $ fig up
  $ firefox http://0.0.0.0:5000/
"""

from os import environ

from flask import Flask

from flask_ratelimiter import RateLimiter
from flask_ratelimiter import ratelimit

app = Flask(__name__)
app.config['RATELIMITER_BACKEND_OPTIONS'] = {
    'host': environ.get('REDIS_HOST', 'localhost')}
ext = RateLimiter(app=app)


@app.route('/')
@ratelimit(3, 1)
def index():
    """Home page."""
    return 'Hello world!  Try to refresh this page several times per second' \
        ' to see the rate limiter in action.'


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
