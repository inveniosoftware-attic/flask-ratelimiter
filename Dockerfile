# This file is part of Flask-RateLimiter
# Copyright (C) 2015 CERN.
#
# Flask-RateLimiter is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -e .[docs,redis]
