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





def password_edit():
    return {}


def password_edit_post():
    app.response.content_type = 'application/json'

    # All names are in lower case by default
    current      = app.request.forms.get('current', '')
    password     = app.request.forms.get('password', '')
    verify       = app.request.forms.get('verify', '')

    # Take the user from the cookie
    user = app.get_user_auth()
    if not user:
        err = 'Auth required'
        return json.dumps({'status':400, 'text':err})
    
    name = user['_id']
    
    # Maybe the user forget something...
    if not name or not password or not verify or not current:
        err = 'All fields are required'
        return json.dumps({'status':400, 'text':err})

    # Look if the passwords match
    if password != verify:
        err = "Passwords desn't match"
        return json.dumps({'status':400, 'text':err})

    # Look if the previous password was good
    print "Look if good?", name, current
    good_current = app.check_auth(name, current)
    print good_current
    if not good_current:
        err = 'Bad current account'
        return json.dumps({'status':403, 'text':err})

    print "Change password", name, password
    # Ok now the current password is good, so we can save the new hash
    app.change_user_password(name, password)
    
    
    return json.dumps({'status':200, 'text':'OK'})
    


pages = {
    # Profile show
    profile:           {'routes': ['/~', '/~:name'], 'view': 'profile', 'static': True, 'wraps': ['classic']},

    # Profile edit
    profile_edit:      {'routes': ['/profile-edit'], 'view': 'profile-edit', 'static': True, 'wraps': ['protected']},
    profile_edit_post: {'routes': ['/profile-edit'], 'method':'POST', 'static': True, 'wraps': ['json']},

    # Password edit
    password_edit:      {'routes': ['/password'], 'view': 'password', 'static': True, 'wraps': ['protected']},
    password_edit_post: {'routes': ['/password'], 'method':'POST', 'static': True, 'wraps': ['json']},

    }
