
import os
import sys
import time
import pymongo
import traceback
import cStringIO

import bottle
# Remove on PROD!
bottle.debug(True)

from bottle import route, view, redirect

from http_helper import helper

# Ok make output debug in errors logs
import sys
sys.stdout = sys.stderr



# A classic page need a real user loggued, and will fill
# the app and user to the template

def do_wrap(wrap_f, f, app):
    def loc_f(**args):
        return wrap_f(f, app, **args)
    return loc_f


def wrap_classic_page(f, app, **args):
    print "WRAPPING FUNCTION", f, app
    user = app.get_user_auth()
    print "Founded user?", user
    r = f(**args)
    r.update({'app' : app, 'user' : user, 'helper' : helper})
    return r


def wrap_protected_page(f, app, **args):
    print "WRAPPING PROTECTED", f, app
    user = app.get_user_auth()
    if not user:
        print "ANONYMOUS ACCES??? GO TO /"
        redirect('/')
        return
    r = f(**args)
    r.update({'app' : app, 'user' : user, 'helper' : helper})
    return r


def wrap_json_page(f, app, **args):
    print "WRAPPING FUNCTION", f, app
    user = app.get_user_auth()
    if not user:
        print "ANONYMOUS ACCES??? GO TO /"
        redirect('/')
        return
    r = f(**args)
    # It's pure json, so no need to touch it
    return r

                    


class WebBackend(object):
    # By default there is no pages lib
    _PAGES_MODULE = None
    # Used to give to __import__ the good lib name
    _MY_LIB_NAME  = ''

    def __init__(self):
        raise NotImplementedError, "WebBackend is an interface!"


    def get_pages_dir(self):
        raise NotImplementedError, "WebBackend is an interface!"


    def get_static(self):
        return 'http://static.shinken.io'


    # Here we will load all pages under the _ourdir_/pages
    # directory. Each one can have a page, views and htdocs dir that we must
    # route correctly
    def load_pages(self):
        # Also load the helper lib, and give him myself
        self.helper = helper
        self.helper.add_app(self)

        print "MY SELF __file__ is", __file__
        pages_dir = os.path.abspath(os.path.dirname(self.__class__._PAGES_MODULE.__file__))
        print "Loading pages directory: %s" % pages_dir

        # Load the common views into the bottle PATH
        common_views = os.path.join(os.path.dirname(pages_dir), 'views')
        print "ADDING COMMON VIEW PATH", common_views
        bottle.TEMPLATE_PATH.append(common_views)

        # Load pages directories
        pages_dirs = [fname for fname in os.listdir(pages_dir)
                      if os.path.isdir(os.path.join(pages_dir, fname))]

        print "Pages dirs", pages_dirs
        sys.path.append(pages_dir)
        # We try to import them, but we keep only the one of
        # our type
        for fdir in pages_dirs:
            print "Try to load", fdir
            mod_path = self.__class__._MY_LIB_NAME+'.pages.%s.%s' % (fdir, fdir)
            try:
                m = __import__(mod_path, fromlist=[mod_path])
                m_dir = os.path.abspath(os.path.dirname(m.__file__))
                sys.path.append(m_dir)

                print "Loaded module m", m
                print m.__file__
                pages = m.pages
                print "Try to load pages", pages
                for (f, entry) in pages.items():
                    routes = entry.get('routes', None)
                    v = entry.get('view', None)
                    wraps = entry.get('wraps', [])

                    # First apply wraps, like "need user and put app/user values"
                    for wrap in wraps:
                        if wrap == 'classic':
                            print "before wrap", f
                            f = do_wrap(wrap_classic_page, f, self)
                            print "New wrap is", f
                        if wrap == 'json':
                            print "before wrap", f
                            f = do_wrap(wrap_json_page, f, self)
                            print "New wrap is", f
                        if wrap == 'protected':
                            print "before wrap", f
                            f = do_wrap(wrap_protected_page, f, self)
                            print "New wrap is", f
                                                                                                                

                    # IMPORTANT: apply VIEW BEFORE route!
                    if v:
                        print "Link function", f, "and view", v
                        f = view(v)(f)

                    # Maybe there is no route to link, so pass
                    if routes:
                        for r in routes:
                            method = entry.get('method', 'GET')
                            print "link function", f, "and route", r, "method", method

                            f = route(r, callback=f, method=method)

                # And we add the views dir of this plugin in our TEMPLATE
                # PATH
                bottle.TEMPLATE_PATH.append(os.path.join(m_dir, 'views'))

                # And finally register me so the pages can get data and other
                # useful stuff
                m.app = self


            except Exception, exp:
                print "*"*200
                print "Loading page: %s" % exp
                print "*"*200
                output = cStringIO.StringIO()
                traceback.print_exc(file=output)
                print "Back trace of this remove: %s" % (output.getvalue())
                output.close()
                
