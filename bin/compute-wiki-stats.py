#!/usr/bin/python

import requests
import json

import os
import sys
import time
import pymongo
import hashlib
import uuid
import ConfigParser
import tarfile
import json
import shutil
from pprint import pprint
import markdown


class GithubDumper():
    def __init__(self, cfg_path):
        self.conf = ConfigParser.SafeConfigParser()
        self.conf.read(cfg_path)
        self.data = self.conf.get('http', 'data')
        self.data_in = self.data+'/in'
        self.data_tmp = self.data+'/tmp'
        self.data_packages = self.data+'/packages'
        self.data_users    = self.data+'/users'
        self.wiki_url      = self.conf.get('wiki', 'url')
        self.wiki_login    = self.conf.get('wiki', 'login')
        self.wiki_password = self.conf.get('wiki', 'password')
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
        # Let's dump wiki users database
        # Beware, under the shinkenio website, the address of the file is not "classic", but
        # in fact you don't need to know the details :)
        headers = {'Host': 'www.shinken-monitoring.org'}
        r = requests.get(self.wiki_url, auth=(self.wiki_login, self.wiki_password), headers=headers)
        
        text = r.text
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith('#') or 'readonly' in line:
                continue
            elts = line.split(':')
            if len(elts) != 5:
                continue
            
            email = elts[3]
            user = self.users.find_one({'email':email})
            if not user:
                continue
            print "WE FOUND ONE VALID", user['_id']
            stats = self.get_user_stats(user['_id'])
            # We can save a write if it's already set
            if stats.get('wiki_account'):
                continue
            # Ok a new one!
            stats['wiki_account'] = True
            self.save_user_stats(user['_id'], stats)
            

        

if __name__ == '__main__':
    g = GithubDumper('/opt/shinken.io/config.ini')
    g.run()

