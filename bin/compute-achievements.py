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



def pack_boy(user, stats):
    return stats.get('nb_packages', 0) > 1

def pack_man(user, stats):
    return stats.get('nb_packages', 0) > 10

def pack_crafter(user, stats):
    return stats.get('nb_packages', 0) > 30

def warchief(user, stats):
    return user['_id'] == 'naparuba'

def community_dev(user, stats):
    return stats.get('org_contribs', 0) > 1

def core_dev(user, stats):
    return stats.get('core_contribs', 0) > 25

def wood_commiter(user, stats):
    return (stats.get('core_contribs', 0) + stats.get('org_contribs', 0)) > 10

def stone_commiter(user, stats):
    return (stats.get('core_contribs', 0) + stats.get('org_contribs', 0)) > 50

def iron_commiter(user, stats):
    return (stats.get('core_contribs', 0) + stats.get('org_contribs', 0)) > 400

def diamond_commiter(user, stats):
    return (stats.get('core_contribs', 0) + stats.get('org_contribs', 0)) > 1000

def doc_writer(user, stats):
    return stats.get('wiki_account', False)

def first_packages_runners(user, stats):
    return user['_id'] in ('frescha','dessaiimrane', 'seb-solon')

def first_packages_winner(user, stats):
    return user['_id'] == 'dessaiimrane'


ACHIEVEMENTS = {'pack-boy': {'f':pack_boy, 'xp':50},
                'pack-man': {'f':pack_man, 'xp':500},
                'pack-crafter' : {'f':pack_crafter, 'xp':1000},
                'warchief' : {'f':warchief, 'xp':500},
                'community-dev' : {'f':community_dev, 'xp':50},
                'core-dev' : {'f':core_dev, 'xp':200},
                'wood-commiter' : {'f':wood_commiter, 'xp':50},
                'stone-commiter' : {'f':wood_commiter, 'xp':250},
                'iron-commiter' : {'f':iron_commiter, 'xp':500},
                'diamond-commiter' : {'f':diamond_commiter, 'xp':1000},
                'doc-writer' : {'f':doc_writer, 'xp':50},
                'first-packages-runners' : {'f':first_packages_runners, 'xp':50},
                'first-packages-winner' : {'f':first_packages_winner, 'xp':100},
               }



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
        for user in self.users.find({'achievements_enabled':True}):
            user_id = user['_id']
            
            print user
            achievements = set(user.get('achievements'))
            
            xp = user.get('xp')
            
            nb_ach = len(achievements)
            print "Computing stats for", user_id, "that got previously", achievements, "and", xp, "XP"
            stats = self.get_user_stats(user_id)
            print "*********%s" % user_id , stats

            for (k,v) in ACHIEVEMENTS.iteritems():
                f = v['f']
                if k not in achievements:
                    print "LOOKING FOR", k, "for", user_id
                    b = f(user, stats)
                    if b:
                        print "GOT IT!", k
                        achievements.add(k)
                        xp += v['xp']
            
            achievements = list(achievements)
            print "Computed achievements", achievements
            print "AND XP", xp
            if len(achievements) != nb_ach:
                user['xp'] = xp
                user['achievements'] = achievements
                self.users.update({'_id':user_id}, user)
            #self.save_user_stats(user_id, stats)
            
    
    def get_user(self, user_name):
        return self.users.find_one({'_id' : user_name})


    def get_pack(self, pname):
        return self.packages.find_one({'_id' : pname})



if __name__ == '__main__':
    s = Achivementer('/opt/shinken.io/config.ini')
    s.run()
