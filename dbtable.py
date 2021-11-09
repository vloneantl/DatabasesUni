from dbconnection import *
from psycopg2.extensions import AsIs
import re


class DbTable:
    dbconn = None

    def __init__(self):
        return

    def table_name(self):
        if re.search("[a-z]{1,9}_", self.dbconn.prefix):
            return self.dbconn.prefix + "table"
        else:
            print("Подозрительный префикс")

    def columns(self):
        return {"test": ["integer", "PRIMARY KEY"]}

    def column_names(self):
        return self.columns().keys()

    def primary_key(self):
        return ['id']

    def column_names_without_id(self):
        lst = self.columns()
        if 'id' in lst:
            del lst['id']
        return lst.keys()

    def table_constraints(self):
        return []

    def create(self):
        sql = "CREATE TABLE " + self.table_name() + "("
        arr = [k + " " + " ".join(v) for k, v in self.columns().items()]
        sql += ", ".join(arr + self.table_constraints())
        sql += ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def drop(self):
        #sql = "DROP TABLE IF EXISTS " + "%s"
        sql = "DROP TABLE IF EXISTS " + self.table_name()
        print(sql)
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, self.table_name())
        self.dbconn.conn.commit()
        return

    def delete_one(self, vals):
        sql = "DELETE FROM " + self.table_name()
        sql += " WHERE {} = %s".format(self.primary_key()[0])
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, vals)
        self.dbconn.conn.commit()
        return

    def insert_one(self, vals):
        for i in range(0, len(vals)):
            if type(vals[i]) != str:
                vals[i] = str(vals[i])
        sql = "INSERT INTO " + self.table_name() + "("
        sql += ", ".join(self.column_names_without_id()) + ") VALUES("
        sql += ", ".join(["%s"]*len(vals)) + ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, vals)
        self.dbconn.conn.commit()
        return

    def first(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()        

    def last(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join([x + " DESC" for x in self.primary_key()])
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()

    def all(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def all_with_limit(self, params):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        sql += " LIMIT "
        sql += "%s"
        sql += " OFFSET "
        sql += "%s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

    def count_all(self):
        sql = "SELECT count(*) FROM " + "%s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, self.table_name())
        return cur.fetchone()
