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

License
=======
Copyright (C) 2014 CERN.

Flask-RateLimiter is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

Flask-RateLimiter is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Flask-RateLimiter; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

In applying this licence, CERN does not waive the privileges and immunities granted to it by virtue of its status as an Intergovernmental Organization or submit itself to any jurisdiction.
