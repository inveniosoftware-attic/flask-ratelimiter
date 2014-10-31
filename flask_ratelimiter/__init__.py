# -*- coding: utf-8 -*-
#
# This file is part of Flask-RateLimiter
# Copyright (C) 2014 CERN.
#
# Flask-RateLimiter is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""
Flask extension
===============

Flask-RateLimiter is initialized like this:

.. code-block:: pycon

    >>> from flask import Flask
    >>> from flask_ratelimiter import RateLimiter
    >>> app = Flask('myapp')
    >>> ext = RateLimiter(app=app)

You can use ratelimit decorator like this:

.. code-block:: pycon

    >>> from flask_ratelimiter import ratelimit
    >>>
    >>> @ratelimit(300, 200)
    >>> def some_view():
    >>>     return 'HelloWorld'

Based on:

* Flask-ext-skeleton

* Snippet of code by Armin Ronacher from:
  http://flask.pocoo.org/snippets/70/
"""

from __future__ import absolute_import

from flask import current_app, request, g
from functools import update_wrapper
from six import iteritems


class RateLimitInfo(object):
    """
    Stores information about rate limiting.
    Can be saved in 'g' object for further use.
    """

    def __init__(self, **kwargs):

        for key, value in iteritems(kwargs):
            setattr(self, key, value)


def on_over_limit(rate_limit_info):
    """
    Default response which will be displayed
    when rate limit is exceeded.
    :param rate_limit_info: RateLimitInfo object
    """
    return "Rate limit was exceeded", 429


class RateLimiter(object):
    """
    Flask extension

    Initialization of the extension:

    .. code-block:: pycon

        >>> from flask import Flask
        >>> from flask_ratelimiter import RateLimiter
        >>> app = Flask('myapp')
        >>> ext = RateLimiter(app=app)

    or alternatively using the factory pattern:

    .. code-block:: pycon

        >>> app = Flask('myapp')
        >>> ext = RateLimiter()
        >>> ext.init_app(app)
    """
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initialize a Flask extension.
        """

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        if 'ratelimiter' in app.extensions:
            raise RuntimeError("Flask application already initialized")
        app.extensions['ratelimiter'] = self

        config = app.config

        config.setdefault('RATELIMITER_BACKEND', 'SimpleRedisBackend')
        config.setdefault('RATELIMITER_BACKEND_OPTIONS', {})
        config.setdefault('RATELIMITER_INJECT_X_HEADERS', True)
        config.setdefault('RATELIMITER_KEY_PREFIX', 'rate_limit')
        self._change_prefix_if_flask_cache(config)

        if config['RATELIMITER_INJECT_X_HEADERS']:
            @app.after_request
            def inject_x_headers(response):
                info = getattr(g, '_rate_limit_info', None)
                if info and info.send_x_headers:
                    h = response.headers
                    h.add('X-RateLimit-Remaining', str(info.remaining))
                    h.add('X-RateLimit-Limit', str(info.limit))
                    h.add('X-RateLimit-Reset', str(info.reset))
                return response

        options = config['RATELIMITER_BACKEND_OPTIONS']
        self.backend = RateLimiter.get_backend(config['RATELIMITER_BACKEND'])(
            **options)

    @staticmethod
    def get_backend(name):
        """
        Returns backend for RateLimiter.
        If there is no such backend, default backend
        will be returned.
        """
        from . import backends
        try:
            backend = getattr(backends, name)
        except AttributeError:
            return getattr(backends, 'SimpleRedisBackend')
        return backend

    def _change_prefix_if_flask_cache(self, config):
        """
        Uses Flask-Cache prefix by default if FlaskCache backend is used.
        """
        if config.get('CACHE_KEY_PREFIX', '') and \
           config.get('RATELIMITER_BACKEND').startswith('FlaskCache'):
            config['RATELIMITER_KEY_PREFIX'] = config['CACHE_KEY_PREFIX']


def ratelimit(limit, per=300, send_x_headers=True,
              over_limit=on_over_limit,
              scope_func=lambda: request.remote_addr,
              key_func=lambda: request.endpoint):
    """
    Decorator can be used for rate limiting.

    Example:

    @ratelimit(30, 10)
    def index():
        return "HelloWorld"
    """
    def decorator(f):
        def rate_limited(*args, **kwargs):
            ratelimiter = current_app.extensions['ratelimiter']
            prefix = current_app.config['RATELIMITER_KEY_PREFIX']
            key = prefix + '/%s/%s/' % (key_func(), scope_func())
            limit_exceeded, remaining, reset = ratelimiter.backend.update(
                key, limit, per)

            info = RateLimitInfo(limit=limit,
                                 per=per,
                                 limit_exceeded=limit_exceeded,
                                 remaining=remaining,
                                 reset=reset,
                                 send_x_headers=send_x_headers)
            g._rate_limit_info = info

            if over_limit is not None and limit_exceeded:
                return over_limit(info)
            return f(*args, **kwargs)
        return update_wrapper(rate_limited, f)
    return decorator


# Version information
from .version import __version__

__all__ = [
    'RateLimiter', '__version__', 'ratelimit'
]
