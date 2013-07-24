#!/usr/bin/python

# -*- coding: utf-8 -*-

# Copyright (C) 2012:
#    Gabes Jean, naparuba@gmail.com
# 

import os
import json

from webgears.bottle import redirect, abort, request, response

### Will be populated by the UI with it's own value
app = None


def give_achievement(name):
    ok_chars = 'azertyuiopqsdfghjklmwxcvbn-_1234567890'
    name = ''.join([c for c in name if c in ok_chars])
    a_dir = os.path.join(app.data_achievements, name)
    if not os.path.exists(a_dir) or not os.path.isdir(a_dir):
        return None
    
    #name = os.path.split(a_dir)
    with open(os.path.join(a_dir, 'how')) as f:
        how = f.read()
    with open(os.path.join(a_dir, 'sub')) as f:
        sub = f.read()
    return {'name':name, 'sub':sub, 'how':how}
    

def achievements():
    a_dir = app.data_achievements
    _achievements = []
    for d in os.listdir(a_dir):
        print "GIVE ACHI?", d
        a = give_achievement(d)
        if a:
            _achievements.append(a)

    # Sort by name instead of this reverse order
    _achievements.reverse()
    return {'achievements' : _achievements}

def achievement(name):
    _achievement = give_achievement(name)
    return {'achievement' : _achievement}

pages = {
    achievements:           {'routes': ['/achievements'], 'view': 'achievements', 'static': False, 'wraps': ['classic']},
    achievement:           {'routes': ['/achievements/:name'], 'view': 'achievement', 'static': False, 'wraps': ['classic']},

    }
