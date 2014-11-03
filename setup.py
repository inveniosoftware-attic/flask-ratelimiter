# -*- coding: utf-8 -*-
#
# This file is part of Flask-RateLimiter
# Copyright (C) 2014 CERN.
#
# Flask-RateLimiter is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

from setuptools import setup
import os
import re
import sys

tests_require_extra = []

if sys.version_info < (2, 7):
    tests_require_extra = ['unittest2']

# Get the version string.  Cannot be done with import!
with open(os.path.join('flask_ratelimiter', 'version.py'), 'rt') as f:
    version = re.search(
        '__version__\s*=\s*"(?P<version>.*)"\n',
        f.read()
    ).group('version')

setup(
    name='Flask-RateLimiter',
    version=version,
    url='http://github.com/inveniosoftware/flask-ratelimiter/',
    license='BSD',
    author='Invenio collaboration',
    author_email='info@invenio-software.org',
    description='Flask-RateLimiter is an extension for Flask '
                'that adds support for rate limiting.',
    long_description=open('README.rst').read(),
    packages=['flask_ratelimiter', 'flask_ratelimiter.backends'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'six',
    ],
    extras_require={
        'docs': ['sphinx'],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Development Status :: 5 - Production/Stable'
    ],
    test_suite='nose.collector',
    tests_require=['nose', 'coverage', 'redis', 'flask_cache'] + tests_require_extra,
)
