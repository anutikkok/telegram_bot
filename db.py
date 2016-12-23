# -*- coding: utf-8 -*-
# make sure it's a new style class
__metaclass__ = type

import sqlite3 as lite
import config
import sys

class SqlMgr:
    def __init__(self):
        self.dbPath = config.database_name
        self.con = None
        self.get_connection(self.dbPath)
    def get_connection(self, dbPath):
        try:
            self.con = lite.connect(dbPath)
            print("connection created")
        except lite.Error as e:
            print("Error %s:" % e.args[0])
            # sys.exit(1)
    def query(self, sql):
        rows = []
        try:
            # with self.con:
            cur = self.con.cursor()
            cur.execute(sql)
            # print "the first element in rows will be the column names."
            column_names = [x[0] for x in cur.description]
            rows.append(column_names)
            while True:
                row = cur.fetchone()
                if row == None:
                    break
                rows.append(row[0])
        except lite.Error as e:
            print("Error %s:" % e.args[0])
        # sys.exit(1)
        return rows

def query(query):
    sqlmgr = SqlMgr()
    #print("the first element in rows will be the column names.")
    rows = sqlmgr.query(query)
    cols = rows.pop(0)


   # print("column names")
    #print(cols)
    #print("data")
    print(rows)
    return rows

