import sys
from prettytable import PrettyTable
from postgre_connection.postgre_db_connection import PostgreConnector
from tables.phones_table import *
from tables.addresses_table import *
sys.path.append('tables')


class Main:

    #config = ProjectConfig()
    connection = PostgreConnector()

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        pt = PeopleTable()
        pht = PhonesTable()
        #dt = DocumentsTable()
        at = AddressesTable()
        pt.create()
        pht.create()
        #dt.create()
        at.create()
        return

    def db_insert_somethings(self):
        pt = PeopleTable()
        pht = PhonesTable()
        at = AddressesTable()
        pt.insert_one(["Test1", "Test2", "Test3"])
        pt.insert_one(["Test4", "Test5", "Test6"])
        pt.insert_one(["Test7", "Test8", "Test9"])
        pht.insert_one([1, "123"])
        pht.insert_one([2, "123"])
        pht.insert_one([3, "123"])
        at.insert_one([1, "a", "b", "c", "d"])

    def db_drop(self):
        pht = PhonesTable()
        pt = PeopleTable()
        #dt = DocumentsTable()
        at = AddressesTable()
        pht.drop()
        #dt.drop()
        pt.drop()
        at.drop()
        return

    def show_main_menu(self):
        menu = """Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - просмотр людей;
    2 - сброс и инициализация таблиц;
    9 - выход."""
        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()

    def after_main_menu(self, next_step):
        if next_step == "2":
            self.db_drop()
            self.db_init()
            self.db_insert_somethings()
            print("Таблицы созданы заново!")
            return "0"
        elif next_step != "1" and next_step != "9" and next_step != "12":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step

    def show_addresses(self):
        if self.person_id == -1:
            while True:
                num = input("Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена):")
                while len(num.strip()) == 0:
                    num = input("Пустая строка. Повторите ввод! Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена):")
                if num == "0":
                    return "1"
                person = PeopleTable().find_by_position(int(num))
                if not person:
                    print("Введено число, неудовлетворяющее количеству людей!")
                else:
                    self.person_id = int(person[0])
                    self.person_obj = person
                    break
        print("Адреса")
        table = PrettyTable(['Id персоны', 'Город', 'Улица', 'Дом', 'Квартира'])
        at = AddressesTable()
        lst = at.all_by_person_id(self.person_id)
        for i in lst:
            table.add_row([str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4])])
        print(table)
        print("""Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат в просмотр людей;
    10 - добавление адреса;
    11 - удаление адреса;
    9 - выход.""")
        return self.read_next_step()

    def show_people(self):
        self.person_id = -1
        print("Список людей")
        table = PrettyTable(['№', 'Фамилия', 'Имя', 'Отчество'])
        lst = PeopleTable().all()
        for i in lst:
            table.add_row([str(i[0]), str(i[1]), str(i[2]), str(i[3])])
        print(table)
        menu = """Дальнейшие операции: 
    0 - возврат в главное меню;
    3 - добавление нового человека;
    4 - удаление человека;
    5 - просмотр телефонов человека;
    8 - просмотр адресов;
    12 - поиск человека по фамилии;
    9 - выход."""
        print(menu)
        return

    def after_show_people(self, next_step):
        while True:
            if next_step == "4":
                pt = PeopleTable()
                pt.del_person()
                return "1"
            elif next_step == "7":
                pt = PhonesTable()
                pt.del_phones_by_id_phones(self.person_id)
                next_step = "5"
            elif next_step == "6":
                pt = PhonesTable()
                phone = input("Введите номер телефона: (0 - отмена): ")
                if phone == "0":
                    return
                while True:
                    try:
                        int(phone)
                    except ValueError:
                        phone = input("Вы ввели не число! Введите номер заново (0 - отмена):").strip()
                        if phone == "0":
                            return
                        continue
                    if len(phone) == 0:
                        phone = input("Вы ничего не ввели! Введите номер заново (0 - отмена):").strip()
                        if phone == "0":
                            return
                    elif len(phone) > 11 | len(phone) < 6:
                        value = input(
                            "Вы ввели неверный формат телефона! Введите номер заново (0 - отмена):").strip()
                        if value == "0":
                            return
                    else:
                        break
                pt.insert_one([self.person_id, phone])
                next_step = "5"
            elif next_step == "5":
                next_step = self.show_phones_by_people()
            elif next_step == '8':
                next_step = self.show_addresses()
            elif next_step == '10':
                at = AddressesTable()
                at.add_address(self.person_id)
                next_step = '8'
            elif next_step == '11':
                at = AddressesTable()
                at.del_address_by_id(self.person_id)
                next_step = '8'
            elif next_step == '12':
                next_step = self.show_person_by_surname()
            elif next_step != "0" and next_step != "9" and next_step != "3":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                return next_step

    def show_add_person(self):
        data = []
        data.append(input("Введите фамилию (1 - отмена): ").strip())
        while True:
            if data[0] == "1":
                return
            if len(data[0].strip()) == 0:
                data[0] = input("Фамилия не может быть пустой! Введите фамилию заново (1 - отмена):").strip()
            if len(data[0].strip()) > 33:
                data[0] = input("Фамилия не может быть такой длинной! Введите фамилию заново (1 - отмена):").strip()
            elif re.search("'|-|;{1,2}", data[0]):
                data[0] = input("Фамилия не может содержать апостроф, двойной дефис или точку с запятой! "
                                "Введите фамилия заново (1 - отмена):").strip()
            else:
                break
        data.append(input("Введите имя (1 - отмена): ").strip())
        while True:
            if data[1] == "1":
                return
            if len(data[1].strip()) == 0:
                data[1] = input("Имя не может быть пустым! Введите имя заново (1 - отмена):").strip()
            if len(data[1].strip()) > 33:
                data[1] = input("Имя не может быть такой длины! Введите имя заново (1 - отмена):").strip()
            elif re.search("'|-|;{1,2}", data[1]):
                data[1] = input("Имя не может содержать апостроф, двойной дефис или точку с запятой! "
                                "Введите имя заново (1 - отмена):").strip()
            else:
                break
        data.append(input("Введите отчество (1 - отмена):").strip())
        if data[2] == "1":
            return
        while True:
            if data[2] == "1":
                return
            if len(data[2].strip()) > 33:
                data[2] = input("Отчество не может быть такой длины! Введите имя заново (1 - отмена):").strip()
            elif re.search("'|-|;{1,2}", data[2]):
                data[2] = input("Отчество не может содержать апостроф, двойной дефис или точку с запятой! "
                                "Введите отчество заново (1 - отмена):").strip()
            else:
                break
        PeopleTable().insert_one(data)
        return

    def show_phones_by_people(self):
        if self.person_id == -1:
            while True:
                num = input("Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена):")
                while len(num.strip()) == 0:
                    num = input("Пустая строка. Повторите ввод! Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена):")
                if num == "0":
                    return "1"
                person = PeopleTable().find_by_position(int(num))
                if not person:
                    print("Введено число, неудовлетворяющее количеству людей!")
                else:
                    self.person_id = int(person[0])
                    self.person_obj = person
                    break
        print("Выбран человек: " + self.person_obj[1] + " " + self.person_obj[2] + " " + self.person_obj[3])
        print("Телефоны:")
        lst = PhonesTable().all_by_person_id(self.person_id)
        for i in lst:
            print(i[1])
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат в просмотр людей;
    6 - добавление нового телефона;
    7 - удаление телефона;
    9 - выход."""
        print(menu)
        return self.read_next_step()

    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while(current_menu != "9"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_people()
                next_step = self.read_next_step()
                current_menu = self.after_show_people(next_step)
            elif current_menu == "2":
                self.show_main_menu()
            elif current_menu == "3":
                self.show_add_person()
                current_menu = "1"
        print("До свидания!")    
        return

    def show_person_by_surname(self):
        data = []
        data.append(input("Введите фамилию (1 - отмена): ").strip())
        while True:
            if data[0] == "1":
                return
            if len(data[0].strip()) == 0:
                data[0] = input("Фамилия не может быть пустой! Введите фамилию заново (1 - отмена):").strip()
            if len(data[0].strip()) > 33:
                data[0] = input("Фамилия не может быть такой длинной! Введите фамилию заново (1 - отмена):").strip()
            elif re.search("'|-|;{1,2}", data[0]):
                data[0] = input("Фамилия не может содержать апостроф, двойной дефис или точку с запятой! "
                                "Введите фамилия заново (1 - отмена):").strip()
            else:
                break
        surname = data[0]
        print("Выбран человек: " + surname)
        table = PrettyTable(['Id персоны', 'Имя', 'Фамилия', 'Отчество'])
        pt = PeopleTable()
        lst = pt.find_by_surname(surname)
        for i in lst:
            table.add_row([str(i[0]), str(i[1]), str(i[2]), str(i[3])])
        print(table)
        menu = """Дальнейшие операции: 
    0 - возврат в главное меню;
    1 - возврат в просмотр людей;
    3 - добавление нового человека;
    4 - удаление человека;
    5 - просмотр телефонов человека;
    8 - просмотр адресов;
    12 - поиск человека по фамилии;
    9 - выход."""
        print(menu)
        return self.read_next_step()

m = Main()
m.main_cycle()
    
