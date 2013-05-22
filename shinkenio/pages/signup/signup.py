#!/usr/bin/python

# -*- coding: utf-8 -*-

# Copyright (C) 2012:
#    Gabes Jean, naparuba@gmail.com
# 


import json

from webgears.bottle import redirect, abort, request, response

### Will be populated by the UI with it's own value
app = None


def signup():
    return {'app' : app, 'err':''}


def signup_post():
    app.response.content_type = 'application/json'

    # We want only characters for name, number and -_ in names. that's all folks
    _name     = app.request.forms.get('name', '').lower()
    name      = ''
    ok_chars = 'azertyuiopqsdfghjklmwxcvbn-_1234567890'
    name = ''.join([c for c in _name if c in ok_chars])

    # Now the others fields
    password = app.request.forms.get('password', '')
    verify   = app.request.forms.get('verify', '')
    email    = app.request.forms.get('email', '')

    # Maybe the user forget something...
    if not name or not password or not verify or not email:
        err = 'All fields are required'
        return json.dumps({'status':400, 'text':err})

    # Look if the passwords match
    if password != verify:
        err = "Passwords desn't match"
        return json.dumps({'status':400, 'text':err})

    # Very basic email thing
    if not "@" in email:
        err = "Invalid email!"
        return json.dumps({'status':400, 'text':err})
        

    # Look if the user is already existing
    u = app.get_user(name)
    if u:
        err = " This user already exists!"
        return json.dumps({'status':400, 'text':err})

    # Ok here we got a valid user
    app.create_user(name, password, email)
    txt = name

    # Ok also login as the user
    app.login_as(name)

    return json.dumps({'status':200, 'text':txt})
    

pages = {
    signup: {'routes': ['/signup'], 'view': 'signup', 'static': True},
    signup_post: {'routes': ['/signup'], 'method':'POST', 'view': 'signup', 'static': True},
    }
