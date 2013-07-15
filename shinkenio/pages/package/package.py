#!/usr/bin/python

# -*- coding: utf-8 -*-

# Copyright (C) 2012:
#    Gabes Jean, naparuba@gmail.com
# 


import json

from webgears.bottle import redirect, abort, request, response

### Will be populated by the UI with it's own value
app = None


def package(name=''):
    # If we ask ~we get our own profile, if we are connected of course
    _package = app.get_package(name)

    return {'package':_package}


def grab(pname=''):
    return app.grab_package(pname)


pages = {
    package:           {'routes': ['/package/:name'], 'view': 'package', 'wraps': ['classic']},
    grab   :           {'routes': ['/grab/:pname'], 'view': None},
    }
