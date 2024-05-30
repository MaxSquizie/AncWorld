from DataBase import Data, Elements
import datetime
db = Data("project")

db.create_table("users",
                "id", "INT",                # айди
                "name", "TEXT",             # фулнэйм
                "nickname", "TEXT",         # ник
                "level", "INT",             # лвл
                "exp", "INT",               # опыт
                "hp", "INT",                # хп
                "mana", "INT",              # мана
                "stamina", "INT",           # выносливость
                "strength", "INT",          # сила
                "agility", "INT",           # ловкость
                "intellect", "INT",         # интеллект
                "luck", "INT",              # удача
                "defence", "INT",           # защита
                "magres", "INT",            # сопротивление магии
                "manareg", "INT",           # регенерация маны
                "hpreg", "INT",             # регенерация хп
                "balance", "INT",           # баланс
                "alive", "BOOL",            # жив/мёртв
                "shoulders", "INT",         # плечи (принимает item_id или None)
                "head", "INT",              # голова (принимает item_id или None)
                "neck", "INT",              # шея (принимает item_id или None)
                "hands", "INT",             # руки (принимает item_id или None)
                "body", "INT",              # тело (принимает item_id или None)
                "waist", "INT",             # талия  (принимает item_id или None)
                "ears", "INT",              # уши (принимает item_id или None)
                "fingers_left", "INT",      # левая кисть (принимает item_id или None)
                "fingers_right", "INT",     # правая кисть (принимает item_id или None)
                "wristle_left", "INT",      # левое запястье (принимает item_id или None)
                "wristle_right", "INT",     # правое запястье (принимает item_id или None)
                "legs", "INT",              # ноги (принимает item_id или None)
                "fight", "TEXT",            # бой (принимает mob_name или None)
                "action", "TEXT",           # процесс (nick, confirm, race, )
                "temp", "TEXT",             # временное значение (что-угодно)
                "pet", "INT",               # пет игрока
                "maunt", "INT",             # маунт игрока
                "race", "TEXT",             # раса
                "class", "TEXT",            # класс
                "rep", "INT",               # репутация
                "sp", "INT",                # доступные очки навыков
                "prof", "TEXT"              # профессии
                )


db.create_table("inv",
                "id", "INT",                # айди игрока
                "item_name", "INT",         # название предмета
                "count", "INT"              # количество
                )


db.create_table("mobs",
                "id", "BIGINT",             # айди
                "mob_name", "TEXT",         # имя монстра
                "rarity", "TEXT",           # тип монстра
                "hp", "INT",                # хп
                "mana", "INT",              # мана
                "strength", "INT",          # сила
                "agility", "INT",           # ловкость
                "intellect", "INT",         # интеллект
                "defence", "INT",           # защита
                "magres", "INT",            # сопротивление магии
                "manareg", "INT"            # регенерация маны
                )


db.create_table("items",
                "id", "BIGINT",             # айди предмета
                "item_name", "TEXT",        # название предмета
                "type", "TEXT",             # оружие/броня/бижа и т.п.
                "cost", "INT",              # цена
                "hp", "INT",                # хп
                "mana", "INT",              # мана
                "stamina", "INT",           # выносливость
                "strength", "INT",          # сила
                "agility", "INT",           # ловкость
                "intellect", "INT",         # интеллект
                "defence", "INT",           # защита
                "magres", "INT",            # сопротивление магии
                "place", "TEXT",            # место экипировки
                "class", "TEXT",            # класс, если предмет имеет ограничение по классу, иначе None
                "onehand", "BOOL",          # одноручное
                "twohand", "BOOL"           # двуручное
                )

db.create_table("PCQ",                      #PlayersCompletedQuests
                "quest_id", "TEXT",
                "player_id", "INT",
                "completed_date", "DATE",
                "got_reward", "BOOL",
                "PRIMARY KEY", "(player_id, quest_id)",
                "FOREIGN KEY", "(player_id) REFERENCES users(id)")

db.create_table("PAQ",                      #PlayersActiveQuests
                "quest_id", "TEXT",
                "player_id", "INTEGER",
                "FOREIGN KEY", "(player_id) REFERENCES users(id)",
                "PRIMARY KEY", "(player_id, quest_id)")



items_db = {
    "1": {
        'name': 'Камень возврата',
        'type': 'artefact',
        'cost': 0
    },
    "2": {
        'name': 'Упырь',
        'type': 'pet',
        'level': 1,
        'atc_mod': 0.3,
        'def_mod': 0.25,
        'damages': [Elements.air.value],
        'crit_damage': 0
    },
    "3": {
        'name': 'Дракон-фамильяр',
        'type': 'pet',
        'level': 30,
        'atc_mod': 1.3,
        'def_mod': 2,
        'damages': [Elements.air.value, Elements.fire.value],
        'crit_damage': 25
    }
}


descriptions = {"desc_1": "Эх, знал бы ты, путник, как я люблю свою работу! Быть почётным стражником в столице... "
                          + "С детства мечтал. Но, порой, в такие жаркие деньки хочется простого человеческого "
                          + "прохладного пива! Жаль, что я не могу покинуть пост ни на минуту до самого вечера "
                          + "\**подмигнул*\*, да и пить во время работы запрещено \**интенсивно подмигивает*\*",
                }


commodity = {"1":
                 {
                    "image": "images/image1.png",
                    "cost": 60,
                    "description": "Хрустящие гренки",
                    "action": "tractir",
                    "item_name": "Гренки"},
             "2":
                 {
                     "image": "images/image2.png",
                     "cost": 40,
                     "description": "Пышный хлеб",
                     "action": "tractir",
                     "item_name": "Хлеб"},
             "3":
                 {
                     "image": "images/image3.png",
                     "cost": 40,
                     "description": "Прохладное пиво",
                     "action": "tractir",
                     "item_name": "Пиво"}
             }



NPCs = {
    "Геральд": {
        "phrase": "Здравствуй, путник. Сыграем в гвинт?",
        "action": None,
        "quests": {
            "1": {
                "name": "Пиво для бравого стражника",
                "description": descriptions["desc_1"],
                "task": "Принести пиво Геральду",
                "required_items": ["Пиво"],
                "required_completed": [],  # Список завершенных квестов, необходимых для доступа к этому квесту
                "reward": {
                    "experience": 123,
                    "money": 123,
                    "reputation": 10
                }
            },
            "2": {
                "name": "name of quest 2",
                "description": "example of description 2",
                "required_completed": ["1"],  # Квест "example2" станет доступен только после завершения квеста "example1"
                "reward": {
                    "experience": 123,
                    "money": 123,
                    "reputation": 10
                }
            },
            "3": {
                "name": "name of quest 3",
                "description": "example of description 3",
                "required_completed": ["example1", "example2"],  # Квест "example3" доступен после завершения "example1" и "example2"
                "reward": {
                    "experience": 123,
                    "money": 123,
                    "reputation": 10
                }
            }
        }
    },

    "Вильям": {
        "phrase": "Здравия желаю!",
        "action": None,
        "quests": None
        },
    "Трактирщик": {
        "phrase": "Чего желаете?",
        "action": "tractir",
        "quests": None,
        "service": "Приобрести предметы"
        },
    'Инженерное дело': {
        "phrase": "В разработке! Доступно Травничество.",
        "action": None,
        "quests": None
        },
    'Кузнечное дело': {
        "phrase": "В разработке! Доступно Травничество.",
        "action": None,
        "quests": None
        },
    'Кожевничество': {
        "phrase": "В разработке! Доступно Травничество.",
        "action": None,
        "quests": None
        },
    'Наложение чар': {
        "phrase": "В разработке! Доступно Травничество.",
        "action": None,
        "quests": None
        },
    'Портняжное дело': {
        "phrase": "В разработке! Доступно Травничество.",
        "action": None,
        "quests": None
        },
    'Алхимия': {
        "phrase": "В разработке! Доступно Травничество.",
        "action": None,
        "quests": None
        },
    'Начертание': {
        "phrase": "В разработке! Доступно Травничество.",
        "action": None,
        "quests": None
        },
    'Ювелирное дело': {
        "phrase": "В разработке! Доступно Травничество.",
        "action": None,
        "quests": None
        },
    'Травничество': {
        "phrase": "ААА",
        "action": None,
        "quests": None
        },
    'Горное дело': {
        "phrase": "В разработке! Доступно Травничество.",
        "action": None,
        "quests": None
        },
    'Снятие шкур': {
        "phrase": "В разработке! Доступно Травничество.",
        "action": None,
        "quests": None
        }
}

quest_ids = [NPCs[i]["quests"] for i in (j for j in NPCs)]


def get_quests_names():
    result = []
    for i in NPCs:
        nps_quest_list = (NPCs[i]['quests'])

        if nps_quest_list != None:
            for j in list(nps_quest_list.keys()):
                result.append(j)
    
    return result


def get_NPCs_names():
    result = []
    nps_quest_list = (NPCs)

    if nps_quest_list != None:
        for j in list(nps_quest_list.keys()):
            result.append(j)

    return result

def quest_check(PAQ, user):
    for i in PAQ:
        for j in NPCs:
            flag = 1
            requiredItems = []
            try:
                for k in NPCs[j]["quests"][i]["required_items"]:
                    if int(db.ReturnValue("inv", "count", parameter=f"WHERE item_name = '{k}' AND id = {user.id}")) > 0:
                        requiredItems.append(k)
                        pass
                    else:
                        flag = 0
                        requiredItems = []
                        break
                if flag:
                    db.fill("PCQ", i, user.id, datetime.date.today(), False, ifNone=False)
                    db.delete("PAQ", "quest_id", i, key_two="player_id", value_two=user.id)
                    for k in requiredItems:
                        db.delete("inv", "id", user.id, key_two="item_name", value_two=k)
            except:
                pass


def get_reward(char, NPC_name, quest_id):
    char.upd_balance(char.get_balance() + NPCs[NPC_name]["quests"][quest_id]["reward"]["money"])
    char.upd_exp(char.get_exp() + NPCs[NPC_name]["quests"][quest_id]["reward"]["experience"])
    char.upd_rep(char.get_rep() + NPCs[NPC_name]["quests"][quest_id]["reward"]["reputation"])


def calculate_damage(attacker_strength, defender_defence):
    damage = max(0, attacker_strength - defender_defence)
    return damage



