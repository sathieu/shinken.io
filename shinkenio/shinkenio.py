#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (C) 2012:
#    Gabes Jean, naparuba@gmail.com


import os
import sys
import time
import pymongo
import hashlib
import uuid
import ConfigParser

from pprint import pprint

mydir = os.path.dirname(__file__)
myroot = os.path.dirname(os.path.dirname(mydir))
sys.path.append(myroot)

# Load ourself
import pages


# And the bottle part
import webgears.bottle as bottle
from webgears.bottle import route, view, request, response, redirect
from webgears.webgears import WebBackend

# And make us outnt in errors log
import sys
sys.stdout = sys.stderr



class ShinkenIO(WebBackend):
    _PAGES_MODULE = pages
    _MY_LIB_NAME  = 'shinkenio'

    def __init__(self, cfg_path):
        # Important : auth secret used for cookie crypting!
        self.auth_secret = '9813813cbe031471896f8b6173f7e61208'
        # Also save bottle libs
        self.request  = request
        self.response = response
        self.redirect = redirect
        config = ConfigParser.RawConfigParser()
        self.conf = config.read(cfg_path)
        self.open_database()


    def open_database(self):
       self.con = pymongo.Connection('localhost')
       print "Shinken.IO Connected to:", self.con
       self.db    = self.con.shinken_io 
       self.users = self.db.users
       self.packs = self.db.packs
       self.modules = self.db.modules

        
    def get_user(self, user_name):
        print "GET USERS", user_name
        u = self.users.find_one({'_id' : user_name})
        print "founded", u
        return u


    def get_user_auth(self):
        print "get_user_auth::", request.get_cookie("user", secret=self.auth_secret)
        # First we look for the user name
        # so we bail out if it's a false one
        user_name = request.get_cookie("user", secret=self.auth_secret)
        # If we cannot check the cookie, bailout
        if not user_name:
            return None
        
        u = self.get_user(user_name)
        print "get_user_auth::return", u
        return u
    
    
    def check_auth(self, user_name, password):
        print "Checking auth of", user_name
        u = self.get_user(user_name)
        if not u:
            print "Warning: UNKOWN USER", user_name
            return False
        # Ok here the user is known, try to compute the hash :)
        print "USER", u
        salt = u['salt']
        pwd_hash = u['pwd_hash']

        # Now compute the user one to see if it's ok
        m = hashlib.sha256()
        m.update(salt)
        m.update(password)
        pwd_hash_to_verify = m.hexdigest()
        print "Hashed password to verify", pwd_hash_to_verify, "with", pwd_hash
        return pwd_hash_to_verify == pwd_hash


    def login_as(self, name):
        # Ok go for a cookie available for 1year
        self.response.set_cookie('user', name, secret=self.auth_secret, path='/', max_age=86400*365)
        



    def create_user(self, name, password, email):
        # First hash the password
        pwd_hash, salt = self.hash_password(password)
        print "PASSWORD HASH", pwd_hash, salt
        
        user = {
            "_id"          : name,
            "email"        : email,
            "creation_time": int(time.time()),
            'pwd_hash'     : pwd_hash,
            'salt'         : salt,
            'full_name'    : '',
            'github'       : '',
            'twitter'      : '',
            'homepage'     : '',
            'api_key'      : uuid.uuid4().get_hex(),
            }
        
        print "Trying to create user", user
        self.users.insert(user)
        print "USER CREATION:", user


    def edit_user(self, name, fullname, email, github, twitter, homepage):
        d = {'full_name':fullname, 'email':email, 'github':github, 'twitter':twitter, 'homepage':homepage}
        print "EDITING USER", d
        self.users.update( { '_id' : name }, { '$set': d})


    def change_user_password(self, name, password):
        pwd_hash, salt = self.hash_password(password)
        d = {'pwd_hash' : pwd_hash, 'salt' : salt}
        self.users.update({ '_id' : name }, { '$set': d})
        

    def hash_password(self, password):
        salt = os.urandom(64).encode('base_64')
        m = hashlib.sha256()
        m.update(salt)
        m.update(password)
        pwd_hash = m.hexdigest()
        return (pwd_hash, salt)
    
    
    def get_gravatar(self, user):
        if not user or not user['email']:
            return "https://secure.gravatar.com/avatar/avatar.jpg"
        email = user['email']
        return "https://secure.gravatar.com/avatar/"+hashlib.md5(email.lower()).hexdigest()
