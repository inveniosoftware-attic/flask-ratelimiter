===================
 Flask-RateLimiter
===================
.. currentmodule:: flask_ratelimiter

.. raw:: html

    <p style="height:22px; margin:0 0 0 2em; float:right">
        <a href="https://travis-ci.org/inveniosoftware/flask-ratelimiter">
            <img src="https://travis-ci.org/inveniosoftware/flask-ratelimiter.png?branch=master"
                 alt="travis-ci badge"/>
        </a>
        <a href="https://coveralls.io/r/inveniosoftware/flask-ratelimiter">
            <img src="https://coveralls.io/repos/inveniosoftware/flask-ratelimiter/badge.png?branch=master"
                 alt="coveralls.io badge"/>
        </a>
    </p>


Flask-RateLimiter is a Flask extension that provides rate limiting
decorator.

.. admonition:: **CAVEAT LECTOR**

   **Flask-RateLimiter is now deprecated in favour of** `Flask-Limiter <https://github.com/alisaifee/flask-limiter>`_

Contents
--------

.. contents::
   :local:
   :depth: 1
   :backlinks: none


Installation
============

Flask-RateLimiter is on PyPI so all you need is:

.. code-block:: console

    $ pip install flask-ratelimiter

The development version can be downloaded from `its page at GitHub
<http://github.com/inveniosoftware/flask-ratelimiter>`_.

.. code-block:: console

    $ git clone https://github.com/inveniosoftware/flask-ratelimiter.git
    $ cd flask-ratelimiter
    $ python setup.py develop
    $ ./run-tests.sh

Requirements
^^^^^^^^^^^^

Flask-RateLimiter has the following dependencies:

* `Flask <https://pypi.python.org/pypi/Flask>`_
* `blinker <https://pypi.python.org/pypi/blinker>`_
* `six <https://pypi.python.org/pypi/six>`_
* Redis or Flask-Cache

Flask-RateLimiter requires Python version 2.6, 2.7 or 3.3+


API
===

This documentation section is automatically generated from
Flask-RateLimiter's source code.

.. automodule:: flask_ratelimiter

.. autoclass:: RateLimiter
   :members:


.. include:: ../CHANGES

.. include:: ../CONTRIBUTING.rst


License
=======

.. include:: ../LICENSE

.. include:: ../AUTHORS
