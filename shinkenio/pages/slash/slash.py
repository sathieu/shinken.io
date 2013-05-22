#!/usr/bin/python

# -*- coding: utf-8 -*-

# Copyright (C) 2012:
#    Gabes Jean, naparuba@gmail.com
# 


from webgears.bottle import redirect, abort, request, response

### Will be populated by the UI with it's own value
app = None


def slash():
    return {}



pages = {
    slash: {'routes': ['/'], 'view': 'slash', 'static': True, 'wraps': ['classic']},
    }
