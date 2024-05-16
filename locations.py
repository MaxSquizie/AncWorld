import sqlite3
import json
from aiogram import types
from aiogram.types import FSInputFile
from DataBase import Data, Get
db = Data("project")

def generate_location(name: str,description: str, peaceful: bool, level: int, attachment: str, mobs, resources,
                            NPCs, sublocations):
    conn = sqlite3.connect('project.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS locs (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        description TEXT,
                        peaceful INT,
                        mobs TEXT,
                        resources TEXT,
                        level INT,
                        NPCs TEXT,
                        sublocations TEXT,
                        attachment TEXT
                    )''')

    attachment = 'images/'+attachment
    mobs_str = None
    resources_str = None
    NPCs_str = None
    sublocations_str = None
    if not (mobs is None):
        mobs_str = json.dumps(mobs)
    if not (resources is None):
        resources_str = json.dumps(resources)
    if not (NPCs is None):
        NPCs_str = json.dumps(NPCs)
    if not (sublocations is None):
        sublocations_str = json.dumps(sublocations)

    c.execute(f"SELECT level FROM locs WHERE description = ?", (description,))
    if c.fetchone() is None:
        c.execute('''INSERT INTO locs (name, description, peaceful, mobs, resources, level, NPCs, sublocations, attachment)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (name, description, peaceful, mobs_str, resources_str, level, NPCs_str, sublocations_str, attachment))

    conn.commit()
    conn.close()






location = {
    "Уэльгард": {
        "name": "Уэльгард",
        "description": 'Вы вошли в Уэльгард.',
        "peaceful": True,
        "level": 1,
        "attachment": 'start_loc.png',
        "mobs": None,
        "resources": None,
        "NPCs": ["Геральд", "Вильям"],
        "sublocations": ["Таверна", "Гильдия профессий"]
    },
    "Таверна": {
        "name": "Таверна",
        "description": 'Вы вошли в таверну.',
        "peaceful": True,
        "level": 1,
        "attachment": 'tavern.png',
        "mobs": None,
        "resources": None,
        "NPCs": ["Трактирщик"],
        "sublocations": ["Уэльгард"]
    },
    "Гильдия профессий": {
        "name": "Гильдия профессий",
        "description": 'Вы вошли в гильдию профессий.',
        "peaceful": True,
        "level": 1,
        "attachment": 'profguild.png',
        "mobs": None,
        "resources": None,
        "NPCs": ['Инженерное дело', 'Кузнечное дело', 'Кожевничество', 'Наложение чар', 'Портняжное дело', 'Алхимия', 'Начертание', 'Ювелирное дело', 'Травничество', 'Горное дело', 'Снятие шкур'],
        "sublocations": ["Уэльгард"]
    }
}

def keyboard_location(location_name, location):
    arr = []
    if location[location_name]["peaceful"] is False:
        arr.append([types.KeyboardButton(text="Атаковать")])
    if not (location[location_name]["resources"] is None):
        arr.append([types.KeyboardButton(text="Профнавык 1"), types.KeyboardButton(text="Профнавык 2"),types.KeyboardButton(text="Профнавык 3")])
    if not (location[location_name]["NPCs"] is None):
        k = 0
        for j in range(len(location[location_name]["NPCs"])//4+int(len(location[location_name]["NPCs"])%4 in [1,2,3])):
            arr.append(list(types.KeyboardButton(text=f"{i}") for i in location[location_name]["NPCs"][k:k+4]))
            k += 4  # счетчик среза чтоб не больше 4 кнопок в ряд
    if not (location[location_name]["sublocations"] is None):
        arr.append(list(types.KeyboardButton(text=f"{i}") for i in location[location_name]["sublocations"]))
    return types.ReplyKeyboardMarkup(keyboard=arr, resize_keyboard=True)

def loc(location_name, message):
    return message.answer_photo(photo=FSInputFile(Get("locs", db.ReturnValue("locs","id", parameter=f"WHERE name = '{location_name}'")).loc_img()),
                                       caption=location[location_name]["description"],
                                       reply_markup=keyboard_location(location_name, location))



for i in location:
    generate_location(*list(location[i][j] for j in location[i]))
