#!/usr/bin/python

# -*- coding: utf-8 -*-

# Copyright (C) 2012:
#    Gabes Jean, naparuba@gmail.com
# 


import json

from webgears.bottle import redirect, abort, request, response

### Will be populated by the UI with it's own value
app = None


def login():
    return {}


def login_post():
    app.response.content_type = 'application/json'

    # All names are in lower case by default
    name     = app.request.forms.get('name', '').lower()
    password = app.request.forms.get('password', '')
    
    # Maybe the user forget something...
    if not name or not password:
        err = 'All fields are required'
        return json.dumps({'status':400, 'text':err})

    # Ok now it's time to check!
    is_auth = app.check_auth(name, password)
    if is_auth:
        app.login_as(name)
        return json.dumps({'status':200, 'text':'OK'})
    else:
        return json.dumps({'status':400, 'text':'Invalid user or Password'})
    

def logout():
    app.response.set_cookie('user', '', secret=app.auth_secret, path='/')
    return {}


pages = {
    login: {'routes': ['/login'], 'view': 'login', 'static': True, 'wraps': ['classic']},
    login_post: {'routes': ['/login'], 'method':'POST', 'view': 'login', 'static': True},
    logout: {'routes': ['/logout'], 'static': True, 'view':'logout', 'wraps': ['classic']},
    }
