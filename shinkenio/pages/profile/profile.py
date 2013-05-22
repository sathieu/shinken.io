#!/usr/bin/python

# -*- coding: utf-8 -*-

# Copyright (C) 2012:
#    Gabes Jean, naparuba@gmail.com
# 


import json

from webgears.bottle import redirect, abort, request, response

### Will be populated by the UI with it's own value
app = None


def profile(name=''):
    # If we ask ~we get our own profile, if we are connected of course
    user = app.get_user_auth()
    if not name:
        user = app.get_user_auth()
        if not user:
            redirect('/')
            return
        _profile = user
    else:
        _profile = app.get_user(name)
        if not _profile:
            redirect('/')
            return
    return {'profile':_profile, 'is_me': user == _profile}


def profile_edit():
    return {}


def profile_edit_post():
    app.response.content_type = 'application/json'

    # All names are in lower case by default
    name     = app.request.forms.get('name', '').strip().lower()
    user = app.get_user_auth()
    if not user or user['_id'] != name:
        err = 'Bad account for updating!'
        return json.dumps({'status':403, 'text':err})

    # Ok now the other fields
    fullname = app.request.forms.get('fullname', '')
    email    = app.request.forms.get('email', '')
    github   = app.request.forms.get('github', '')
    twitter  = app.request.forms.get('twitter', '')
    homepage = app.request.forms.get('homepage', '')
    
    app.edit_user(name, fullname, email, github, twitter, homepage)
    return json.dumps({'status':200, 'text':'OK'})
    


pages = {
    profile:           {'routes': ['/~', '/~:name'], 'view': 'profile', 'static': True, 'wraps': ['classic']},
    profile_edit:      {'routes': ['/profile-edit'], 'view': 'profile-edit', 'static': True, 'wraps': ['protected']},
    profile_edit_post: {'routes': ['/profile-edit'], 'method':'POST', 'static': True, 'wraps': ['json']},
    }
