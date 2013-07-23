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



class Stater():
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

    def save_user_stats(self, uid, stats):
        user_dir = os.path.join(self.data_users, uid)
        if not os.path.exists(user_dir):
            os.mkdir(user_dir)
            os.chmod(user_dir, 0o755)
            
        p = os.path.join(self.data_users, uid, 'stats.json')
        buf = json.dumps(stats)
        f = open(p, 'w')
        f.write(buf)
        f.close()
        


    def run(self):
        print "Starting to compute the stats", self.data_in
        for user in self.users.find():
            print "Computing stats for", user
            user_id = user['_id']
            stats = self.get_user_stats(user_id)
            print "*********%s" % user_id , stats
            user_packages = self.packages.find({'user_id':user_id})
            stats['nb_packages'] = 0
            for p in user_packages:
                stats['nb_packages'] += 1
                types = {}
                print "Package found", p['_id']
                for t in p.get('types', []):
                    nb = types.get(t, 0) + 1
                    types[t] = nb
                for t in types:
                    k = 'nb_%ss' % t
                    nb = stats.get(k, 0) + 1
                    stats[k] = nb
            
            print "Computed stats", stats
            self.save_user_stats(user_id, stats)


    
    def assume_string(self, s):
        if not isinstance(s, basestring):
            return ''
        try:
            return s.encode('utf8', 'ignore')
        except:
            return ''



    def assume_list_of_strings(self, l):
        r = []
        if not isinstance(l, list):
            return []
        for s in l:
            r.append(self.assume_string(s))
        return r


    def clean_name(self, name):
        ok_chars = 'azertyuiopqsdfghjklmwxcvbn-_1234567890'
        return ''.join([c for c in name if c in ok_chars])
        
    
        
    def get_user(self, user_name):
        return self.users.find_one({'_id' : user_name})


    def get_pack(self, pname):
        return self.packages.find_one({'_id' : pname})



if __name__ == '__main__':
    s = Stater('/opt/shinken.io/config.ini')
    s.run()
