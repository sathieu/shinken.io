# Lib for getting raw data into a Customer database.

import pymongo
import time

class DataGetter(object):
    def __init__(self):
        pass

    def get_raw_data(self, db_host, cust_id, host_id):
        self.con = pymongo.Connection(db_host)
        self.db = getattr(self.con, cust_id)
        raw_data = self.db.raw_data

        # Ok we got the raw_data collection, now search for a data
        # with this name
        s = [i for i in raw_data.find({'host_id' : host_id}).sort('timestamp', pymongo.DESCENDING).limit(1)]
        e = s[0]
        if not e:
            return None
        return e


    def get_data(self, db_host, cust_id, host_id, name):
        self.con = pymongo.Connection(db_host)
        self.db = getattr(self.con, cust_id)
        raw_data = self.db.raw_data
        
        # Ok we got the raw_data collection, now search for a data
        # with this name
        s = [i for i in raw_data.find({'host_id' : host_id}, {name : 1}).sort('timestamp', pymongo.DESCENDING).limit(1)]
        e = s[0]
        if not e:
            return None
        return e.get(name, None)
                        
