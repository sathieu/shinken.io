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
        self.github_login  = self.conf.get('github', 'login')
        self.github_password  = self.conf.get('github', 'password')
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
        # First dump core contribs
        r = requests.get('https://api.github.com/repos/naparuba/shinken/contributors', auth=(self.github_login, self.github_password))

        contribs = json.loads(r.text)


        user_gravatars = {}
        for u in self.users.find():
            mail = u['email']
            if mail:
                h = hashlib.md5(mail.lower()).hexdigest()
                user_gravatars[h] = u['_id']

        print "GRAVATAR REVERSE", user_gravatars
        for c in contribs:
            uname = c['login']
            contributions = c['contributions']
            gravatar_id   = c['gravatar_id']
            print uname, contributions, gravatar_id
            user_id = user_gravatars.get(gravatar_id)
            if user_id:
                stats = self.get_user_stats(user_id)
                stats['core_contribs'] = contributions
                print "NEW STATS", stats
                self.save_user_stats(user_id, stats)

        org_contribs = {}
        for page in range(1, 10):
            r = requests.get('https://api.github.com/orgs/shinken-monitoring/repos?page=%d&per_page=100' % page, auth=(self.github_login, self.github_password))
            repos = json.loads(r.text)

            print "GRAVATAR REVERSE", user_gravatars
            
            for repo in repos:
                contributors_url = repo['contributors_url']
                print contributors_url
                r = requests.get(contributors_url, auth=(self.github_login, self.github_password))
                if r.status_code != 200:
                    continue
                contribs = json.loads(r.text)
                for c in contribs:
                    print "C", c
                    try:
                        uname = c['login']
                    except:
                        print r.headers
                        raise
                    contributions = c['contributions']
                    gravatar_id   = c['gravatar_id']
                    print uname, contributions, gravatar_id
                    user_id = user_gravatars.get(gravatar_id)
                    if user_id:
                        old = org_contribs.get(user_id, 0)
                        org_contribs[user_id] = old + contributions
        print "TOTAL ORG CONTRIBS", org_contribs
        for (user_id, nb) in org_contribs.iteritems():
            stats = self.get_user_stats(user_id)
            stats['org_contribs'] = nb
            print "NEW STATS", stats
            self.save_user_stats(user_id, stats)
        

        

if __name__ == '__main__':
    g = GithubDumper('/opt/shinken.io/config.ini')
    g.run()

