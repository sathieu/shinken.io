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



def browse_packs_updated():
    packages = app.get_all_packs_updated()
    return {'results' : packages}



def browse_modules_updated():
    packages = app.get_all_modules_updated()
    return {'results' : packages}



def browse_starred():
    packages = app.get_all_most_starred()
    return {'results' : packages}


pages = {
    browse_packs_updated: {'routes': ['/browse/packs/updated'], 'method': 'GET', 'view': 'browse_packs_updated', 'static': False , 'wraps': ['classic']},
    browse_modules_updated: {'routes': ['/browse/modules/updated'], 'method': 'GET', 'view': 'browse_modules_updated', 'static': False , 'wraps': ['classic']},
    browse_starred: {'routes': ['/browse/starred'], 'method': 'GET', 'view': 'browse_starred', 'static': False , 'wraps': ['classic']},

         }
