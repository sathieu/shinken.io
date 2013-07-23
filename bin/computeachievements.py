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
import json
import shutil
from pprint import pprint



class Achivementer():
    def __init__(self, cfg_path):
        self.conf = ConfigParser.SafeConfigParser()
        self.conf.read(cfg_path)
        self.data = self.conf.get('http', 'data')
        self.data_in = self.data+'/in'
        self.data_tmp = self.data+'/tmp'
        self.data_packages = self.data+'/packages'
        self.data_users = self.data+'/users'
        self.open_database()
    
    
    def open_database(self):
        self.con = pymongo.Connection('localhost')
        print "Shinken.IO Connected to:", self.con
        self.db    = self.con.shinken_io 
        self.users = self.db.users
        self.packages = self.db.packages
        self.modules = self.db.modules


    def get_user_stats(self, uid):
        p = os.path.join(self.data_users, uid, 'stats.json')
        if os.path.exists(p):
            print "LOADING USER STATS", p
            f = open(p)
            buf = f.read()
            f.close()
            return json.loads(buf)
        return {}



    def run(self):
        print "Starting to compute the achievements"
        for user in self.users.find():

            user_id = user['_id']
            print user
            achievements = set(user.get('achievements'))
            print "Computing stats for", user, "that got previously", achievements
            stats = self.get_user_stats(user_id)
            print "*********%s" % user_id , stats
            
            
            achievements = list(achievements)
            print "Computed achievements", achievements
            #self.users.update({'_id':user_id}, {'achievements': achievements})
            #self.save_user_stats(user_id, stats)
            
    
    def get_user(self, user_name):
        return self.users.find_one({'_id' : user_name})


    def get_pack(self, pname):
        return self.packages.find_one({'_id' : pname})



if __name__ == '__main__':
    s = Achivementer('/opt/shinken.io/config.ini')
    s.run()
