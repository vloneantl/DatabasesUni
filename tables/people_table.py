from dbtable import *

from tables.phones_table import PhonesTable


class PeopleTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "people"

    def columns(self):
        return {"id": ["SERIAL", "PRIMARY KEY"],
                "last_name": ["varchar(32)", "NOT NULL"],
                "first_name": ["varchar(32)", "NOT NULL"],
                "second_name": ["varchar(32)"]}

    def find_by_position(self, num):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        sql += " LIMIT 1 OFFSET " + "%s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, str(num - 1))
        return cur.fetchone()

    def find_by_surname(self, surname):
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE last_name = " + "'" + surname + "'"
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        #print(sql)
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, str(surname))
        return cur.fetchall()

    def del_person(self):
        st = """Удаление человека: 
    Введите id человека: """
        id = input(st).strip()
        while True:
            try:
                int(id)
            except ValueError:
                id = input("Введено не число! Введите id заново (0 - отмена):").strip()
                if id == "0":
                    return
                continue
            if len(id) == 0:
                id = input("Ничего не введено! Введите id заново (0 - отмена):").strip()
                if id == "0":
                    return
            else:
                break
        self.delete_one([id])
