#!/usr/bin/python

# -*- coding: utf-8 -*-

# Copyright (C) 2009-2012:
#    Gabes Jean, naparuba@gmail.com

import os
import json
import uuid

from webgears.bottle import redirect, abort, request, response

### Will be populated by the UI with it's own value
app = None


def search_cli():
    app.response.content_type = 'application/json'
    print "CLI: Trying to search for a package by tags", app.request.GET.__dict__
    tags_raw = app.request.GET.get('keywords', '')
    tags = [t.strip() for t in tags_raw.split(',')]
    
    print "CLI: We wil finally search for", tags
    
    res = []
    # Ok here it's a valid user :)
    
    packages = app.search(keywords=tags)

    print "The app return us", packages

    for p in packages:
        res.append({'name':p['_id'], 'user_id':p['user_id'],
                    'description':p['description'], 'keywords':p['keywords'],
                    })
    
    return json.dumps({'status': 200, 'result': res})


pages = {search_cli: {'routes': ['/searchcli'], 'method': 'GET', 'view': None, 'static': False},
         }
