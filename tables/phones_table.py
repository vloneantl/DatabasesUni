from dbtable import *


class PhonesTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "phones"

    def columns(self):
        return {"person_id": ["integer", "REFERENCES prj_people(id) ON DELETE CASCADE"],
                "phone": ["varchar(12)", "NOT NULL"]}
    
    def primary_key(self):
        return ['person_id', 'phone']    

    def table_constraints(self):
        return ["PRIMARY KEY(person_id, phone)"]

    def all_by_person_id(self, pid):
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE person_id = " + "%s"
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, str(pid))
        return cur.fetchall()

    def delete_one(self, vals):
        sql = "DELETE FROM " + self.table_name()
        sql += " WHERE {} = %s".format(self.primary_key()[0])
        sql += " AND {} = %s".format(self.primary_key()[1])
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, vals)
        self.dbconn.conn.commit()
        return

    def del_phones_by_id_phones(self, person_id):
        vals = []
        vals.append(str(person_id))
        vals.append(input("    Введите номер телефона => ").strip())
        while True:
            if vals[1] == "0":
                return
            try:
                int(vals[1])
            except ValueError:
                vals[1] = input("Введено не число! Введите номер телефона заново (0 - отмена):").strip()
                continue
            if len(vals[1]) == 0:
                vals[1] = input("Ничего не введено! Введите номер телефона заново (0 - отмена):").strip()
            elif len(vals[1]) > 12 | len(vals[1]) < 6:
                vals[1] = input("Неверный формат телефона! Введите номер телефона заново (0 - отмена):").strip()
            else:
                break
        self.delete_one(vals)
