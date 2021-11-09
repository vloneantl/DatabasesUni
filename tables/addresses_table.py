from dbtable import *

import re
import datetime

from tables.people_table import PeopleTable


class AddressesTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "addresses"

    def columns(self):
        return {"person_id": ["integer", "REFERENCES prj_people(id) ON DELETE CASCADE"],
                "city": ["varchar(32)", "NOT NULL"],
                "street": ["varchar(64)", "NOT NULL"],
                "house_number": ["varchar(10)", "NOT NULL"],
                "flat_number": ["varchar(10)", "NOT NULL"]}

    def primary_key(self):
        return ['person_id', 'city', 'street', 'house_number', 'flat_number']

    def table_constraints(self):
        return ["PRIMARY KEY(person_id, city, street, house_number, flat_number)"]

    def all_by_person_id(self, pid):
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE person_id = "+"%s"
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, str(pid))
        return cur.fetchall()

    def delete_one(self, vals):
        sql = "DELETE FROM " + self.table_name()
        sql += " WHERE {} = %s".format(self.primary_key()[0])
        sql += " AND {} = %s".format(self.primary_key()[1])
        sql += " AND {} = %s".format(self.primary_key()[2])
        sql += " AND {} = %s".format(self.primary_key()[3])
        sql += " AND {} = %s".format(self.primary_key()[4])
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, vals)
        self.dbconn.conn.commit()
        return

    def add_address(self, pid):
        data = []
        data.append(str(pid))
        data.append(input("Введите город (1 - отмена): ").strip())
        while True:
            if data[1] == "1":
                return
            if len(data[1].strip()) == 0:
                data[1] = input("Поле Город не может быть пустым! "
                                "Введите Город заново (1 - отмена):").strip()
            if len(data[1].strip()) > 32 | len(data[1].strip()) < 10:
                data[1] = input(
                    "Город не может быть таким длинным! Введите серию и номер заново (1 - отмена):").strip()
            elif re.search("'|-|;{1,2}", data[1]):
                data[1] = input("Город не могут содержать апостроф, двойной дефис или точку с запятой! "
                                "Введите город заново (1 - отмена):").strip()
            else:
                break
        data.append(input("Введите улицу (1 - отмена): ").strip())
        while True:
            if data[2] == "1":
                return
            if len(data[2].strip()) == 0:
                data[2] = input("Поле Улица не может быть пустой! "
                                "Введите улицу заново (1 - отмена):").strip()
            if len(data[2].strip()) > 64:
                data[2] = input(
                    "Улица не может быть такой длинной! Введите улицу заново (1 - отмена):").strip()
            elif re.search("'|-|;{1,2}", data[2]):
                data[2] = input("Улица не может содержать апостроф, двойной дефис или точку с запятой! "
                                "Введите тип документов заново (1 - отмена):").strip()
            else:
                break
        data.append(input("Введите номер дома (1 - отмена): ").strip())
        while True:
            if data[3] == "1":
                return
            if len(data[3].strip()) == 0:
                data[3] = input("Номер дома не может быть пустым! "
                                "Введите номер дома заново (1 - отмена):").strip()
            if len(data[3].strip()) > 10:
                data[3] = input(
                    "Номер дома не может быть таким длины! Введите Номер дома заново (1 - отмена):").strip()
            elif re.search("'|-|;{1,2}", data[3]):
                data[3] = input("Номер дома не может содержать апостроф, двойной дефис или точку с запятой! "
                                "Введите номер дома заново (1 - отмена):").strip()
            else:
                break
        data.append(input("Введите номер квартиры (1 - отмена): ").strip())
        while True:
            if data[4] == "1":
                return
            if len(data[4].strip()) == 0:
                data[4] = input("Номер квартиры не может быть пустым! "
                                "Введите номер квартиры заново (1 - отмена):").strip()
            if len(data[4].strip()) > 10:
                data[4] = input(
                    "Номер квартиры не может быть таким длины! Введите место выдачи номер квартиры "
                    "заново (1 - отмена):").strip()
            elif re.search("'|-|;{1,2}", data[4]):
                data[4] = input("Номер квартиры не может содержать апостроф, двойной дефис или точку "
                                "с запятой! Введите номер квартиры заново (1 - отмена):").strip()
            else:
                break
        at = AddressesTable()
        at.insert_one(data)
        return

    def del_address_by_id(self, pid):
        vals = []
        vals.append(pid)
        vals.append(input("Введите город: ").strip())
        while True:
            if vals[1] == "0":
                return
            if len(vals[1]) == 0:
                vals[1] = input("Ничего не введено! Введите город заново (0 - отмена):").strip()
            else:
                break
        vals.append(input("Введите улицу: ").strip())
        while True:
            if vals[1] == "0":
                return
            if len(vals[1]) == 0:
                vals[1] = input("Ничего не введено! Введите улицу заново (0 - отмена):").strip()
            else:
                break
        vals.append(input("Введите номер дома: ").strip())
        while True:
            if vals[1] == "0":
                return
            if len(vals[1]) == 0:
                vals[1] = input("Ничего не введено! Введите номер дома заново (0 - отмена):").strip()
            else:
                break
        vals.append(input("Введите номер квартиры: ").strip())
        while True:
            if vals[1] == "0":
                return
            if len(vals[1]) == 0:
                vals[1] = input("Ничего не введено! Введите номер квартиры заново (0 - отмена):").strip()
            else:
                break
        self.delete_one(vals)
