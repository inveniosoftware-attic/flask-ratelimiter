.. _quickstart:

Quickstart
==========

This guide assumes you have successfully installed Flask-RateLimiter and a working
understanding of Flask. If not, follow the installation steps and read about
Flask at http://flask.pocoo.org/docs/.


A Minimal Example
-----------------

A minimal Flask-RateLimiter usage example looks like this. First create the
application and initialize the extension:

>>> from flask import Flask
>>> from flask_ratelimiter import RateLimiter
>>> app = Flask('myapp')
>>> ext = RateLimiter(app=app)

>>> CHANGEME

.. literalinclude:: ../tests/helpers.py
