import sqlite3
import os
from enum import Enum
from aiogram.fsm.state import State, StatesGroup

path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/" )



class Elements(Enum):
    earth = 1
    fire = 2
    water = 3
    air = 4

class Data:


    def __init__(self,dbname):

        print("БД работает")

        """Инициализируем базу данных"""  

        # Подключаемся к БД
        self.db = sqlite3.connect(f'{path}/{dbname}.db')

        # Создаем курсор
        self.cur = self.db.cursor()

        

    def create_table(self, table_name, *args):

        """Создает стол с заданными столбцами"""

        # выполняем SQL-запрос для создания таблицы
        columns = ", ".join([f"{arg} {args[i+1]}" for i, arg in enumerate(args) if i%2 == 0])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.db.execute(query)
        # сохраняем изменения и закрываем соединение
        self.db.commit()




    #peer id, имя таблицы, уникальный идентификатор, значение, аргументы
    def fill(self, table_name, *args, ifNone=True):

        """Заполняем таблицу"""
        
        #вытаскиваем значение из бд
        self.cur.execute(f"SELECT * FROM {table_name}")
        first_column = self.cur.description[0][0]
        self.cur.execute(f"SELECT {first_column} FROM {table_name} WHERE {first_column} = ?", (tuple(args)[0],))
        #вопросики
        quantity = (len(args)-1)*"?,"+"?"
        #если значения нет, то записываем
        if self.cur.fetchone() is None and ifNone:
            self.cur.execute(f"INSERT INTO {table_name} VALUES ({quantity})", (tuple(args)))
            #сохраняем
            self.db.commit()
        #записываем даже если есть значение
        else:
            self.cur.execute(f"INSERT INTO {table_name} VALUES ({quantity})", (tuple(args)))
            # сохраняем
            self.db.commit()

            #print("Пользователь добавлен!")

    def delete(self, table_name, key, value, key_two = None, value_two = None):
        if key_two is None:
            self.cur.execute(f"DELETE from {table_name} WHERE {key} = {value}")
        else:
            self.cur.execute(f"DELETE from {table_name} WHERE {key} = {value} AND {key_two} = {value_two}")
        self.db.commit()
        #print("Данные удалены!")

    def ReturnValue(self,tablename, setvalue, parameter = None):
        try:
            self.cur.execute(f"SELECT {setvalue} FROM {tablename} {parameter}")               #WHERE {wherevalue} = {parameter}"):
            result = list(self.cur.fetchall()[0])
            if len(result) == 1:
                result = result[0]
                if str(result).isdigit():
                    result = int(result)
            return result
        except:
            return ""

    def UpdateValue(self, tablename, nowvalue, newvalue, parameter=None):
        self.cur.execute(f'UPDATE {tablename} SET {nowvalue} = "{newvalue}" {parameter}')
        self.db.commit()
        #print("Данные обновлены")


class Get:
    def __init__(self, tablename, id):
        self.db = Data("project")
        self.id = id
        self.table = tablename

    def nick(self):
        db = self.db
        id = self.id
        tablename = self.table
        return db.ReturnValue(tablename=tablename, setvalue="nickname", parameter=f"WHERE id = {id}")

    def action(self):
        db = self.db
        id = self.id
        tablename = self.table
        return db.ReturnValue(tablename=tablename, setvalue="action", parameter=f"WHERE id = {id}")

    def temp(self):
        db = self.db
        id = self.id
        tablename = self.table
        return db.ReturnValue(tablename=tablename, setvalue="temp", parameter=f"WHERE id = {id}")

    def race(self):
        db = self.db
        id = self.id
        tablename = self.table
        return db.ReturnValue(tablename=tablename, setvalue="race", parameter=f"WHERE id = {id}")

    def hp(self):
        db = self.db
        id = self.id
        tablename = self.table
        return db.ReturnValue(tablename=tablename, setvalue="hp", parameter=f"WHERE id = {id}")

    def mana(self):
        db = self.db
        id = self.id
        tablename = self.table
        return db.ReturnValue(tablename=tablename, setvalue="mana", parameter=f"WHERE id = {id}")

    def stamina(self):
        db = self.db
        id = self.id
        tablename = self.table
        return db.ReturnValue(tablename=tablename, setvalue="stamina", parameter=f"WHERE id = {id}")

    def strength(self):
        db = self.db
        id = self.id
        tablename = self.table
        return db.ReturnValue(tablename=tablename, setvalue="strength", parameter=f"WHERE id = {id}")

    def agility(self):
        db = self.db
        id = self.id
        tablename = self.table
        return db.ReturnValue(tablename=tablename, setvalue="agility", parameter=f"WHERE id = {id}")

    def intellect(self):
        db = self.db
        id = self.id
        tablename = self.table
        return db.ReturnValue(tablename=tablename, setvalue="intellect", parameter=f"WHERE id = {id}")

    def luck(self):
        db = self.db
        id = self.id
        tablename = self.table
        return db.ReturnValue(tablename=tablename, setvalue="luck", parameter=f"WHERE id = {id}")

    def defence(self):
        db = self.db
        id = self.id
        tablename = self.table
        return db.ReturnValue(tablename=tablename, setvalue="defence", parameter=f"WHERE id = {id}")

    def balance(self):
        db = self.db
        id = self.id
        tablename = self.table
        return db.ReturnValue(tablename=tablename, setvalue="balance", parameter=f"WHERE id = {id}")

    def exp(self):
        db = self.db
        id = self.id
        tablename = self.table
        return db.ReturnValue(tablename=tablename, setvalue="exp", parameter=f"WHERE id = {id}")

    def rep(self):
        db = self.db
        id = self.id
        tablename = self.table
        return db.ReturnValue(tablename=tablename, setvalue="balance", parameter=f"WHERE id = {id}")

    def lvl(self):
        db = self.db
        id = self.id
        tablename = self.table
        return db.ReturnValue(tablename=tablename, setvalue="level", parameter=f"WHERE id = {id}")

    def sp(self):
        db = self.db
        id = self.id
        tablename = self.table
        return db.ReturnValue(tablename=tablename, setvalue="sp", parameter=f"WHERE id = {id}")

    def loc_img(self):
        db = self.db
        id = self.id
        tablename = self.table
        return db.ReturnValue(tablename=tablename, setvalue="attachment", parameter=f"WHERE id = {id}")

class Upd:
    def __init__(self, tablename, id):
        self.db = Data("project")
        self.id = id
        self.table = tablename

    def action(self, newvalue):
        db = self.db
        id = self.id
        tablename = self.table
        db.UpdateValue(tablename=tablename, nowvalue="action", newvalue=newvalue, parameter=f"WHERE id = {id}")

    def temp(self, newvalue):
        db = self.db
        id = self.id
        tablename = self.table
        db.UpdateValue(tablename=tablename, nowvalue="temp", newvalue=newvalue, parameter=f"WHERE id = {id}")

    def nick(self, newvalue):
        db = self.db
        id = self.id
        tablename = self.table
        db.UpdateValue(tablename=tablename, nowvalue="nickname", newvalue=newvalue, parameter=f"WHERE id = {id}")

    def race(self, newvalue):
        db = self.db
        id = self.id
        tablename = self.table
        db.UpdateValue(tablename=tablename, nowvalue="race", newvalue=newvalue, parameter=f"WHERE id = {id}")

    def hp(self, newvalue):
        db = self.db
        id = self.id
        tablename = self.table
        db.UpdateValue(tablename=tablename, nowvalue="hp", newvalue=newvalue, parameter=f"WHERE id = {id}")

    def mana(self, newvalue):
        db = self.db
        id = self.id
        tablename = self.table
        db.UpdateValue(tablename=tablename, nowvalue="mana", newvalue=newvalue, parameter=f"WHERE id = {id}")

    def stamina(self, newvalue):
        db = self.db
        id = self.id
        tablename = self.table
        db.UpdateValue(tablename=tablename, nowvalue="stamina", newvalue=newvalue, parameter=f"WHERE id = {id}")

    def strength(self, newvalue):
        db = self.db
        id = self.id
        tablename = self.table
        db.UpdateValue(tablename=tablename, nowvalue="strength", newvalue=newvalue, parameter=f"WHERE id = {id}")

    def agility(self, newvalue):
        db = self.db
        id = self.id
        tablename = self.table
        db.UpdateValue(tablename=tablename, nowvalue="agility", newvalue=newvalue, parameter=f"WHERE id = {id}")

    def intellect(self, newvalue):
        db = self.db
        id = self.id
        tablename = self.table
        db.UpdateValue(tablename=tablename, nowvalue="intellect", newvalue=newvalue, parameter=f"WHERE id = {id}")

    def luck(self, newvalue):
        db = self.db
        id = self.id
        tablename = self.table
        db.UpdateValue(tablename=tablename, nowvalue="luck", newvalue=newvalue, parameter=f"WHERE id = {id}")

    def defence(self, newvalue):
        db = self.db
        id = self.id
        tablename = self.table
        db.UpdateValue(tablename=tablename, nowvalue="defence", newvalue=newvalue, parameter=f"WHERE id = {id}")

    def balance(self, newvalue):
        db = self.db
        id = self.id
        tablename = self.table
        db.UpdateValue(tablename=tablename, nowvalue="balance", newvalue=newvalue, parameter=f"WHERE id = {id}")

    def exp(self, newvalue):
        db = self.db
        id = self.id
        tablename = self.table
        db.UpdateValue(tablename=tablename, nowvalue="exp", newvalue=newvalue, parameter=f"WHERE id = {id}")

    def rep(self, newvalue):
        db = self.db
        id = self.id
        tablename = self.table
        db.UpdateValue(tablename=tablename, nowvalue="rep", newvalue=newvalue, parameter=f"WHERE id = {id}")

    def lvl(self, newvalue):
        db = self.db
        id = self.id
        tablename = self.table
        db.UpdateValue(tablename=tablename, nowvalue="level", newvalue=newvalue, parameter=f"WHERE id = {id}")

    def sp(self, newvalue):
        db = self.db
        id = self.id
        tablename = self.table
        db.UpdateValue(tablename=tablename, nowvalue="sp", newvalue=newvalue, parameter=f"WHERE id = {id}")

class Character:
    def __init__(self, tablename, id):
        self.id = id
        self.table = tablename
        self.upd = Upd(tablename, id)
        self.get = Get(tablename, id)

    def get_nick(self):
        get = self.get
        return get.nick()

    def get_action(self):
        get = self.get
        return get.action()

    def get_temp(self):
        get = self.get
        return get.temp()

    def get_race(self):
        get = self.get
        return get.race()

    def get_hp(self):
        get = self.get
        return get.hp()

    def get_mana(self):
        get = self.get
        return get.mana()

    def get_stamina(self):
        get = self.get
        return get.stamina()

    def get_strength(self):
        get = self.get
        return get.strength()

    def get_agility(self):
        get = self.get
        return get.agility()

    def get_intellect(self):
        get = self.get
        return get.intellect()

    def get_luck(self):
        get = self.get
        return get.luck()

    def get_defence(self):
        get = self.get
        return get.defence()

    def get_balance(self):
        get = self.get
        return get.balance()

    def get_exp(self):
        get = self.get
        return get.exp()

    def get_rep(self):
        get = self.get
        return get.rep()

    def get_lvl(self):
        get = self.get
        return get.lvl()

    def get_sp(self):
        get = self.get
        return get.sp()

    def upd_action(self, newvalue):
        upd = self.upd
        upd.action(newvalue)

    def upd_temp(self, newvalue):
        upd = self.upd
        upd.temp(newvalue)

    def upd_nick(self, newvalue):
        upd = self.upd
        upd.nick(newvalue)

    def upd_race(self, newvalue):
        upd = self.upd
        upd.race(newvalue)

    def upd_hp(self, newvalue):
        upd = self.upd
        upd.hp(newvalue)

    def upd_mana(self, newvalue):
        upd = self.upd
        upd.mana(newvalue)

    def upd_stamina(self, newvalue):
        upd = self.upd
        upd.stamina(newvalue)

    def upd_strength(self, newvalue):
        upd = self.upd
        upd.strength(newvalue)

    def upd_agility(self, newvalue):
        upd = self.upd
        upd.agility(newvalue)

    def upd_intellect(self, newvalue):
        upd = self.upd
        upd.intellect(newvalue)

    def upd_luck(self, newvalue):
        upd = self.upd
        upd.luck(newvalue)

    def upd_defence(self, newvalue):
        upd = self.upd
        upd.defence(newvalue)

    def upd_balance(self, newvalue):
        upd = self.upd
        upd.balance(newvalue)

    def upd_exp(self, newvalue):
        upd = self.upd
        upd.exp(newvalue)

    def upd_rep(self, newvalue):
        upd = self.upd
        upd.rep(newvalue)

    def upd_lvl(self, newvalue):
        upd = self.upd
        upd.lvl(newvalue)

    def upd_sp(self, newvalue):
        upd = self.upd
        upd.sp(newvalue)


mob_data = {
    "Дикий пёс": {
        "name": "Дикий пёс",
        "rarity": "Обычный",
        "hp": 50,
        "mana": 10,
        "strength": 5,
        "agility": 12,
        "intellect": 5,
        "defence": 2,
        "magres": 4,
        "manareg": 2
    },
}


class Mob:
    def __init__(self, name):
        mob_info = mob_data.get(name, {})
        self.name = mob_info.get("name", "")
        self.rarity = mob_info.get("rarity", "")
        self.hp = mob_info.get("hp", 0)
        self.mana = mob_info.get("mana", 0)
        self.strength = mob_info.get("strength", 0)
        self.agility = mob_info.get("agility", 0)
        self.intellect = mob_info.get("intellect", 0)
        self.defence = mob_info.get("defence", 0)
        self.magres = mob_info.get("magres", 0)
        self.manareg = mob_info.get("manareg", 0)


class FightStates(StatesGroup):
    fighting = State()
