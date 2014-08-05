===================
 Flask-RateLimiter
===================

.. image:: https://travis-ci.org/inveniosoftware/flask-ratelimiter.png?branch=master
    :target: https://travis-ci.org/inveniosoftware/flask-ratelimiter
.. image:: https://coveralls.io/repos/inveniosoftware/flask-ratelimiter/badge.png?branch=master
    :target: https://coveralls.io/r/inveniosoftware/flask-ratelimiter
.. image:: https://pypip.in/v/Flask-RateLimiter/badge.png
   :target: https://pypi.python.org/pypi/Flask-RateLimiter/
.. image:: https://pypip.in/d/Flask-RateLimiter/badge.png
   :target: https://pypi.python.org/pypi/Flask-RateLimiter/

About
=====
Flask-RateLimiter is a Flask extension that provides rate limiting
decorator.

Installation
============
Flask-RateLimiter is on PyPI so all you need is: ::

    pip install Flask-RateLimiter

Documentation
=============
Documentation is readable at http://flask-ratelimiter.readthedocs.org or can be built using Sphinx: ::

    git submodule init
    git submodule update
    pip install Sphinx
    python setup.py build_sphinx

Testing
=======
Running the test suite is as simple as: ::

    python setup.py test

or, to also show code coverage: ::

    ./run-tests.sh
