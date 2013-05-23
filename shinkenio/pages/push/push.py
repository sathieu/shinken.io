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


# LIMIT file at 5MB, quite good for compress file isns't it?
# Even the WebUI is only 3.7MB
LIMIT = 5000000


def push():
    app.response.content_type = 'application/json'
    print "Trying to push a new file", app.request.forms.__dict__
    api_key = app.request.forms.get('api_key')
    data = app.request.files.get('data')
    print "KEY", api_key
    
    if not api_key:
        return json.dumps({'status':401, 'text': 'Error : there is no api key!'})

    if not data:
        return json.dumps({'status':400, 'text':'Error : I think you miss something like... data maybe?'})

    # ok there is something to look at
    user = app.get_user_from_api_key(api_key)

    # not a good user api? get out and get back with a real one...
    if not user:
        return json.dumps({'status' : 403, 'text' : 'Error: bad api key. A typo maybe?'})

    # Ok here it's a valid user :)

    raw = data.file.read(LIMIT)
    over = data.file.read(1)
    # Only take the last part of the name if the user try to trick us...
    filename = os.path.split(data.filename)[1]
    if over:
        return json.dumps({'status': 400, 'text': 'Sorry your file is too big! The limit is %sb'%LIMIT})

    name = user.get('_id')
    app.save_pushed_pack(name, filename, raw)
    return json.dumps({'status': 200, 'text': 'Hi %s, your file is uploaded! It will be available soon' % name})


pages = {push: {'routes': ['/push'], 'method': 'POST', 'view': None, 'static': True},
         }
