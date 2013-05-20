#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012:
#    Gabes Jean, naparuba@gmail.com
#
# This file is part of MyMonitoringBox, all rights reserved.

import time
import copy
import math
from pprint import pprint
try:
    import json
except ImportError:
    # For old Python version, load
    # simple json (it can be hard json?! It's 2 functions guy!)
    try:
        import simplejson as json
    except ImportError:
        print "Error: you need the json or simplejson module"
        raise



class Helper(object):
    def __init__(self):
        self.app = None

    def add_app(self, app):
        self.app = app
        self.static = self.app.get_static()
        

    def act_inactive(self, b):
        if b:
            return 'Active'
        else:
            return 'Inactive'

    def yes_no(self, b):
        if b:
            return 'Yes'
        else:
            return 'No'

    def print_float(self, f):
        return '%.2f' % f


    def ena_disa(self, b):
        if b:
            return 'Enabled'
        else:
            return 'Disabled'

    # For a unix time return something like
    # Tue Aug 16 13:56:08 2011
    def print_date(self, t):
        if t == 0 or t == None:
            return 'N/A'
        return time.asctime(time.localtime(t))


    # For a time, print something like
    # 10m 37s  (just duration = True)
    # N/A if got bogus number (like 1970 or None)
    # 1h 30m 22s ago (if t < now)
    # Now (if t == now)
    # in 1h 30m 22s
    # Or in 1h 30m (no sec, if we ask only_x_elements=2, 0 means all)
    def print_duration(self, t, just_duration=False, x_elts=0):
        if t == 0 or t == None:
            return 'N/A'
        #print "T", t
        # Get the difference between now and the time of the user
        seconds = int(time.time()) - int(t)

        # If it's now, say it :)
        if seconds == 0:
            return 'Now'

        in_future = False

        # Remember if it's in the future or not
        if seconds < 0:
            in_future = True

        # Now manage all case like in the past
        seconds = abs(seconds)
        #print "In future?", in_future

        #print "sec", seconds
        seconds = long(round(seconds))
        #print "Sec2", seconds
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        weeks, days = divmod(days, 7)
        months, weeks = divmod(weeks, 4)
        years, months = divmod(months, 12)

        minutes = long(minutes)
        hours = long(hours)
        days = long(days)
        weeks = long(weeks)
        months = long(months)
        years = long(years)

        duration = []
        if years > 0:
            duration.append('%dy' % years)
        else:
            if months > 0:
                duration.append('%dM' % months)
            if weeks > 0:
                duration.append('%dw' % weeks)
            if days > 0:
                duration.append('%dd' % days)
            if hours > 0:
                duration.append('%dh' % hours)
            if minutes > 0:
                duration.append('%dm' % minutes)
            if seconds > 0:
                duration.append('%ds' % seconds)

        #print "Duration", duration
        # Now filter the number of printed elements if ask
        if x_elts >= 1:
            duration = duration[:x_elts]

        # Maybe the user just want the duration
        if just_duration:
            return ' '.join(duration)

        # Now manage the future or not print
        if in_future:
            return 'in ' + ' '.join(duration)
        else:  # past :)
            return ' '.join(duration) + ' ago'




    # Return a button with text, image, id and class (if need)
    def get_button(self, text, img=None, id=None, cls=None):
        #s = '<div class="buttons">\n'
        s = '<div class="btn">\n'
        if cls and not id:
            s += '<div class="%s">\n' % cls
        elif id and not cls:
            s += '<div id="%s">\n' % id
        elif id and cls:
            s += '<div class="%s" id="%s">\n' % (cls, id)
        else:
            s += '<div>\n'
        if img:
            s += '<img src="%s" alt=""/>\n' % img
        s += "%s" % text
        s += ''' </div>
            </div>\n'''

        return s




    
    def get_input_bool(self, b, id=None):
        id_s = ''
        if id:
            id_s = 'id="%s"' % id
        if b:
            return """<input type="checkbox" checked="checked" %s/>\n""" % id_s
        else:
            return """<input type="checkbox" %s />\n""" % id_s





    # Get
    def get_navi(self, total, pos, step=30):
        step = float(step)
        nb_pages = math.ceil(total / step)
        current_page = int(pos / step)

        step = int(step)

        res = []

        if nb_pages == 0 or nb_pages == 1:
            return None

        if current_page >= 2:
            # Name, start, end, is_current
            res.append((u'« First', 0, step, False))
            res.append(('...', None, None, False))

        print "Range,", current_page - 1, current_page + 1
        for i in xrange(current_page - 1, current_page + 2):
            if i < 0:
                continue
            print "Doing PAGE", i
            is_current = (i == current_page)
            start = int(i * step)
            # Maybe we are generating a page too high, bail out
            if start > total:
                continue

            end = int((i+1) * step)
            res.append(('%d' % (i+1), start, end, is_current))

        if current_page < nb_pages - 2:
            start = int((nb_pages - 1) * step)
            end = int(nb_pages * step)
            res.append(('...', None, None, False))
            res.append((u'Last »', start, end, False))

        print "Total:", total, "pos", pos, "step", step
        print "nb pages", nb_pages, "current_page", current_page

        print "Res", res

        return res


    # TODO: Will look at the string s, and return a clean output without
    # danger for the browser
    def strip_html_output(self, s):
        return s


    # We want the html id of an hostor a service. It's basically
    # the full_name with / changed as -- (because in html, / is not valid :) )
    def get_html_id(self, elt):
        return self.get_full_name(elt).replace('/', '--').replace(' ', '_').replace('.', '_')


    # URI with spaces are BAD, must change them with %20
    def get_uri_name(self, elt):
        return self.get_full_name(elt).replace(' ', '%20')




helper = Helper()
