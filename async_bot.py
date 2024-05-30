import asyncio
import datetime
import json
import locations
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram import F, MagicFilter
import datas as dt
import DataBase as DB
from locations import *
import keyboards as kb
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token="6589229979:AAGtrAUUDTWV1Bh8DFXt3TIWTBlC_EAkAqE")
# in_builder = InlineKeyboardBuilder()
dp = Dispatcher()
quest_names = dt.get_quests_names()
NPCs_names = dt.get_NPCs_names()
backslash = "\n"
@dp.message(Command("start"))
async def cmd_answer(message: types.Message):
    user = message.from_user
    if db.ReturnValue("users", "nickname",parameter=f"WHERE id = {user.id}") == "":
        await message.answer(
            "Добро пожаловать!\n\nЧтобы начать ваше приключение, дайте вашему будущему герою имя.\nВведите никнейм, под которым вы хотели бы быть известным в AncWorld!", keyboard = None)
        db.fill("users", user.id, user.username, "Неизвестный игрок", 1, 0, 100, 100, 0, 0, 0, 0, 0, 0, 0, 5, 5, 100,
                True, None, None, None, None, None, None, None, None, None, None, None, None, None, "nick", None, None,
                None, None, None, 0, 5, "")
        db.fill("inv", user.id, dt.items_db["1"]["name"], 1)
        db.fill("PAQ", '',user.id)
        db.fill("PCQ", '', user.id, '', False)
    else:
        await message.answer("Дважды начать не получится!", keyboard = None)


@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    await message.answer_photo(FSInputFile('images/menu.png'), reply_markup=kb.set_menu)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@dp.message(Command("photo"))
async def send_photo(message: types.Message):
    await message.answer_photo(FSInputFile('images/start_loc.png'))


@dp.message(lambda message: message.text == 'Атаковать')
async def initiate_fight(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = Get('users', user_id)

    mob = DB.Mob("Дикий пёс")
    character = DB.Character('users', user_id)
    print("1")
    await state.update_data(mob=mob)
    print("2")
    await state.update_data(character=character)

    await message.answer(
        f"Вы начали бой с {mob.name}.\n\n"
        f"Ваше состояние:\n"
        f"HP: {character.get_hp()}\n"
        f"Мана: {character.get_mana()}\n\n"
        f"Состояние противника:\n"
        f"HP: {mob.hp}\n"
        f"Мана: {mob.mana}",
        reply_markup=InlineKeyboardMarkup(row_width=2, inline_keyboard=([[InlineKeyboardButton(text='Атаковать', callback_data='attack_turn')]])))

    await state.set_state(DB.FightStates.fighting)


@dp.message()
async def message_handler(message: types.Message):
    msg = message.text
    user = message.from_user
    char = DB.Character("users", user.id)
    # a = await user.get_profile_photos()
    # print(a.photos[0][1].file_id)

    action = char.get_action()
    db.cur.execute(f"SELECT * FROM PAQ WHERE player_id = {user.id}")
    PAQ = list(i[0] for i in db.cur.fetchall())
    dt.quest_check(PAQ, user)

    if action == "nick":
        if len(msg) > 16:
            await message.answer("Этот имя слишком длинное, укажите ник длиной до 16 символов.")
        elif len(msg) < 3:
            await message.answer("Этот имя слишком короткое, укажите ник длиной от 3 символов.")
        else:
            await message.answer(f"Вы уверены, что хотите выбрать именно этот никнейм - {msg} - для вашего персонажа?",
                                 reply_markup=kb.confirm_keyboard)
        char.upd_action("confirm")
        char.upd_temp(msg)

    elif action == "confirm":
        if msg.lower() == "да":
            char.upd_nick(char.get_temp())
            char.upd_temp(None)
            char.upd_action("racing")
            await message.answer(
                f"Прекрасно, {char.get_nick()}! Теперь выберите расу вашего персонажа. Учтите, что у каждой расы есть свои плюсы, а будущий класс может как дополнять её, так и обременять. Хотя кто знает, сколько странных, но не менее эффективных сборок ещё предстоит собрать игрокам :)",
                reply_markup=kb.race_keyboard)
        else:
            await message.answer("Выберите имя своему герою.")
            await db.UpdateValue("users", "action", "nick", parameter=f"WHERE id = {user.id}")

    elif action == "racing":
        if msg.lower() == "эльф":
            await message.answer("Эльфы - прирождённые лучники. Уверены в этом выборе?",
                                 reply_markup=kb.confirm_keyboard)
            char.upd_action("conf")
            char.upd_temp("эльф")
        if msg.lower() == "гном":
            await message.answer("Гномы сильны как танки и ремесленники. Уверены в этом выборе?",
                                 reply_markup=kb.confirm_keyboard)
            char.upd_action("conf")
            char.upd_temp("гном")
        if msg.lower() == "человек":
            await message.answer("Люди - сильные воины. Уверены в этом выборе?", reply_markup=kb.confirm_keyboard)
            char.upd_action("conf")
            char.upd_temp("человек")
        if msg.lower() == "орк":
            await message.answer("Орки известны как яростные берсерки. Уверены в этом выборе?",
                                 reply_markup=kb.confirm_keyboard)
            char.upd_action("conf")
            char.upd_temp("орк")
        if msg.lower() == "нежить":
            await message.answer("Нежить всегда показывает невероятные высоты в магии и защите. Уверены в этом выборе?",
                                 reply_markup=kb.confirm_keyboard)
            char.upd_action("conf")
            char.upd_temp("нежить")
        if msg.lower() == "халфлинг":
            await message.answer("Халфлинги часто асоциируются с внезапной смертью от клинка. Уверены в этом выборе?",
                                 reply_markup=kb.confirm_keyboard)
            char.upd_action("conf")
            char.upd_temp("халфлинг")

    elif action == "conf":
        if msg.lower() == "да":
            char.upd_race(char.get_temp())
            char.upd_action(None)
            char.upd_temp(None)
            await message.answer(f"Успешно! Достигните высот в AncWorld, {char.get_race()} {char.get_nick()}")
            char.upd_action("Уэльгард")
            await message.answer_photo(photo=FSInputFile(Get("locs",1).loc_img()),
                                       caption=location["Уэльгард"]["description"],
                                       reply_markup=keyboard_location("Уэльгард", location, user))

        else:
            await message.answer(f"Правильно, лучше посмотреть всё!", reply_markup=kb.race_keyboard)
            char.upd_action("racing")

    elif action in list(loc_name for loc_name in location):
        flag = 1
        if msg in list(loc_name for loc_name in location):
            await loc(msg, message, user)
            char.upd_action(msg)

        elif msg in list(NPC_name for NPC_name in dt.NPCs):
            for loc_name in location:
                if flag:
                    for NPC_name in location[loc_name]["NPCs"]:
                        if msg == NPC_name and action == loc_name and flag:
                            if dt.NPCs[NPC_name]["quests"] is None:
                                try:
                                    await message.answer(f"{msg}:\n\n{dt.NPCs[msg]['phrase']}",
                                                            reply_markup=InlineKeyboardMarkup(
                                                            row_width=1,
                                                            inline_keyboard=[
                                                            [InlineKeyboardButton(
                                                                text=f"{dt.NPCs[NPC_name]['service']}",
                                                                callback_data=f'{dt.NPCs[NPC_name]["action"]}')]]))
                                except:
                                    await message.answer(f"{msg}:\n\n{dt.NPCs[msg]['phrase']}")
                            else:
                                for i in dt.NPCs[NPC_name]["quests"]:
                                    RC = dt.NPCs[NPC_name]["quests"][i]["required_completed"]
                                    db.cur.execute(f"SELECT * FROM PCQ WHERE player_id = {user.id}")
                                    PCQ = list(i[0] for i in db.cur.fetchall())
                                    db.cur.execute(f"SELECT * FROM PAQ WHERE player_id = {user.id}")
                                    PAQ = list(i[0] for i in db.cur.fetchall())
                                    parameter = dt.NPCs[NPC_name]["action"]
                                    if flag:
                                        if i in PCQ and not db.ReturnValue("PCQ", "got_reward", parameter=f"WHERE player_id = {user.id} AND quest_id = '{i}'"):
                                            await message.answer(f"{msg}:\n\n{dt.NPCs[msg]['phrase']}", reply_markup=kb.quest_button(i, parameter=parameter, PCQ=True))
                                            break

                                        elif RC == [] and not (i in PAQ) and not (i in PCQ):
                                            await message.answer(f"{msg}:\n\n{dt.NPCs[msg]['phrase']}", reply_markup=kb.quest_button(i, parameter=parameter))
                                            break

                                        else:
                                            for j in RC:
                                                if (j not in PCQ and j not in PAQ or j == "") and flag:
                                                    pass
                                                else:
                                                    flag = 0
                                                    try:
                                                        await message.answer(f"{msg}:\n\n{dt.NPCs[msg]['phrase']}",
                                                                             reply_markup=InlineKeyboardMarkup(row_width=1,
                                                                                                               inline_keyboard=[
                                                                                                                   [
                                                                                                                       InlineKeyboardButton(
                                                                                                                           text=f"{dt.NPCs[NPC_name]['service']}",
                                                                                                                           callback_data=f'{dt.NPCs[NPC_name]["action"]}'
                                                                                                                       )], ]
                                                                                                               ))
                                                    except:
                                                        await message.answer(f"{msg}:\n\n{dt.NPCs[msg]['phrase']}")
                                            if flag and RC != []:
                                               await message.answer(f"{msg}:\n\n{dt.NPCs[msg]['phrase']}", reply_markup=kb.quest_button(i))



    elif action in NPCs_names:
        if msg == "Принять":
            db.fill("PAQ", str(char.get_temp()), user.id)
            for i in location:
                for j in location[i]["NPCs"]:
                    if action in j:
                        char.upd_temp(i)
            char.upd_action(char.get_temp())
            char.upd_temp("")
            await message.answer("Задание принято!")
            await loc(char.get_action(), message, user)


@dp.callback_query(lambda c: c.data == 'characteristic')
async def show_characteristics(callback_query: types.CallbackQuery, caption=None):
    user_id = callback_query.from_user.id
    char = DB.Character('users', user_id)

    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Выносливость', callback_data='upgrade_stamina')],
        [InlineKeyboardButton(text='Сила', callback_data='upgrade_strength')],
        [InlineKeyboardButton(text='Ловкость', callback_data='upgrade_agility')],
        [InlineKeyboardButton(text='Интеллект', callback_data='upgrade_intellect')],
        [InlineKeyboardButton(text='Удача', callback_data='upgrade_luck')],
        [InlineKeyboardButton(text="Назад",callback_data='menu'),
         InlineKeyboardButton(text="Закрыть",callback_data='closed')]])

    if not (caption is None):
        characteristics_message = caption+"\n"\
                                  f"Ваши характеристики:\n" \
                                  f"Выносливость: {char.get_stamina()}\n" \
                                  f"Сила: {char.get_strength()}\n" \
                                  f"Ловкость: {char.get_agility()}\n" \
                                  f"Интеллект: {char.get_intellect()}\n" \
                                  f"Удача: {char.get_luck()}\n" \
                                  f"Доступные очки навыков: {char.get_sp()}\n"
    else:
        characteristics_message = f"Ваши характеристики:\n" \
                                  f"Выносливость: {char.get_stamina()}\n" \
                                  f"Сила: {char.get_strength()}\n" \
                                  f"Ловкость: {char.get_agility()}\n" \
                                  f"Интеллект: {char.get_intellect()}\n" \
                                  f"Удача: {char.get_luck()}\n" \
                                  f"Доступные очки навыков: {char.get_sp()}\n"

    await bot.edit_message_media(types.InputMediaPhoto(media=FSInputFile('images/menu.png'), caption=characteristics_message),
                                 chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id, reply_markup=inline_kb)

@dp.callback_query(lambda c: c.data.startswith('upgrade_'))
async def upgrade_characteristic(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    character = DB.Character("users", user_id)
    sp = character.get_sp()

    if sp > 0:
        characteristic = callback_query.data.split('_')[1]
        current_value = getattr(character, f'get_{characteristic}')()
        getattr(character, f'upd_{characteristic}')(current_value + 1)
        character.upd_sp(sp - 1)

        await show_characteristics(callback_query, f"{characteristic.capitalize()} увеличена на 1.")
    else:
        await callback_query.answer(text="У вас недостаточно очков навыков.",show_alert=True)


@dp.callback_query(lambda c: c.data == "attack_turn", DB.FightStates.fighting)
async def fight_turn(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    character = data['character']
    mob = data['mob']
    print(callback_query.data)
    # Вычисляем урон
    char_damage = dt.calculate_damage(character.get_strength(), mob.defence)
    mob.hp -= char_damage

    mob_damage = dt.calculate_damage(mob.strength, character.get_defence())
    character_hp = character.get_hp() - mob_damage
    character.upd_hp(character_hp)

    # Проверяем состояние боя
    if mob.hp <= 0:
        await callback_query.message.edit_text(
            f"Вы победили {mob.name}!\n\n"
            f"Ваше состояние:\n"
            f"HP: {character_hp}\n"
            f"Мана: {character.get_mana()}",
        )
        character.upd_hp(100 + character.get_stamina() * 10)
        await state.clear()
    elif character_hp <= 0:
        await callback_query.message.edit_text(
            f"Вы проиграли {mob.name}.\n\n"
            f"Ваше состояние:\n"
            f"HP: 0\n"
            f"Мана: {character.get_mana()}",
        )
        character.upd_hp(100 + character.get_stamina()*10)
        await state.clear()
    else:
        await callback_query.message.edit_text(
            f"Вы нанесли {char_damage} урона {mob.name}.\n"
            f"{mob.name} нанес вам {mob_damage} урона.\n\n"
            f"Ваше состояние:\n"
            f"HP: {character_hp}\n"
            f"Мана: {character.get_mana()}\n\n"
            f"Состояние противника:\n"
            f"HP: {mob.hp}\n"
            f"Мана: {mob.mana}",
            reply_markup=InlineKeyboardMarkup(row_width=2, inline_keyboard=([[InlineKeyboardButton(text='Атаковать', callback_data='attack_turn')]])))



@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    user = callback.from_user
    char = DB.Character("users", user.id)
    if callback.data == "closed":
        id = user.id
        await callback.answer('Вы закрыли меню.', show_alert=True)
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)

    if callback.data == "char":
        await bot.edit_message_media(types.InputMediaPhoto(media=FSInputFile('images/menu.png')), chat_id=callback.message.chat.id,
                                     message_id=callback.message.message_id, reply_markup=kb.char_menu)

    if callback.data == "bag":
        query = "SELECT item_name, count FROM inv WHERE id = ?"
        db.cur.execute(query, (user.id,))
        inventory = db.cur.fetchall()

        if inventory:
            inventory_message = "Ваш инвентарь:\n"
            for item_name, count in inventory:
                inventory_message += f"{item_name}: {count}\n"
        else:
            inventory_message = "Ваш инвентарь пуст."

        await bot.send_message(user.id, inventory_message)

    if callback.data == "skills":
        await bot.edit_message_media(types.InputMediaPhoto(media=FSInputFile('images/menu.png')),
                                     chat_id=callback.message.chat.id,
                                     message_id=callback.message.message_id, reply_markup=kb.skill_menu)

    if callback.data == "ability":
        await callback.answer('У вас пока нет умений.', show_alert=True)


    if callback.data == "arts":
            await callback.answer('У вас пока нет артефактов.', show_alert=True)

    if callback.data == "equipment":
        await callback.answer('Отображение экипировки ещё не готово!', show_alert=True)

    if callback.data == "profs":
        await callback.answer('У вас нет профессий.', show_alert=True)

    if callback.data == "pet":
        await callback.answer('У вас нет питомца.', show_alert=True)

    if callback.data == "menu":
        await bot.edit_message_media(types.InputMediaPhoto(media=FSInputFile('images/menu.png')), chat_id=callback.message.chat.id,
                                     message_id=callback.message.message_id, reply_markup=kb.set_menu)

    if callback.data in quest_names:  #in dt.quest_ids[0]:
        NPC_name = ""
        for i in dt.NPCs:
            if NPC_name == "":
                for j in dt.NPCs[i]["quests"]:
                    if j == callback.data:
                        NPC_name = i
                        break
        for i in location:
            if NPC_name in location[i]["NPCs"]:
                char.upd_action(NPC_name)
        char.upd_temp(callback.data)
        await bot.send_message(chat_id=callback.message.chat.id, text=f'***{dt.NPCs[NPC_name]["quests"][callback.data]["name"]}***'
                                                                      f'\n\n'
                                                                      f'{dt.NPCs[NPC_name]["quests"][callback.data]["description"]}'
                                                                      f'\n\n'
                                                                      f'*Задание*: {dt.NPCs[NPC_name]["quests"][callback.data]["task"]}'
                                                                      f'\n\n'
                                                                      f'*Награда:*\n'
                                                                      f'Опыт: '
                                                                      f'{dt.NPCs[NPC_name]["quests"][callback.data]["reward"]["experience"]}'
                                                                      f'\nШекели: '
                                                                      f'{dt.NPCs[NPC_name]["quests"][callback.data]["reward"]["money"]}'
                                                                      f'\nРепутация: '
                                                                      f'{dt.NPCs[NPC_name]["quests"][callback.data]["reward"]["reputation"]}',
                                                                      reply_markup=kb.apply_menu, parse_mode="Markdown")

    elif callback.data == "tractir":
        char.upd_temp(1)
        await bot.send_photo(chat_id=callback.message.chat.id, photo=types.FSInputFile(dt.commodity[str(char.get_temp())]['image']),
                             caption=dt.commodity[str(char.get_temp())]['description'],
                             reply_markup=kb.carousel_menu(char))

    elif callback.data == "left":
        char.upd_temp(char.get_temp()-1)
        await bot.edit_message_media(media=types.InputMediaPhoto(media=FSInputFile(dt.commodity[str(char.get_temp())]['image']),
                                                           caption=dt.commodity[str(char.get_temp())]['description']),
                                     chat_id=callback.message.chat.id,
                                     message_id=callback.message.message_id,
                                     reply_markup=kb.carousel_menu(char))

    elif callback.data == "right":
        char.upd_temp(char.get_temp()+1)
        try:
            await bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=types.InputMediaPhoto(
                    media=FSInputFile(dt.commodity[str(char.get_temp())]["image"]),
                    caption=dt.commodity[str(char.get_temp())]["description"]
                ),
                reply_markup=kb.carousel_menu(char)
            )
        except TelegramBadRequest:
            await bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=types.InputMediaPhoto(
                    media=FSInputFile(dt.commodity[str(char.get_temp())]["image"]),
                    caption= dt.commodity[str(char.get_temp())]["description"]
                ),
                reply_markup=kb.carousel_menu(char)
            )

    elif callback.data == "buy":
        print(char.get_balance(), dt.commodity[str(char.get_temp())]["cost"])
        if char.get_balance() >= int(dt.commodity[str(char.get_temp())]["cost"]):
            char.upd_balance(char.get_balance()-int(dt.commodity[str(char.get_temp())]["cost"]))
            if db.ReturnValue("inv", "count", parameter=f'WHERE item_name = {dt.commodity[str(char.get_temp())]["item_name"]}') == "":
                db.fill("inv", user.id, dt.commodity[str(char.get_temp())]["item_name"], 1, ifNone=False)
            else:
                db.UpdateValue("inv", "count", db.ReturnValue("inv", "count", parameter=f'WHERE item_name = {dt.commodity[str(char.get_temp())]["item_name"]}')+1, parameter=f'WHERE item_name = {dt.commodity[str(char.get_temp())]["item_name"]}')
            await bot.send_message(chat_id=callback.message.chat.id, text=f"Успешно! Остаток баланса: {char.get_balance()}")
        else:
            await bot.send_message(chat_id=callback.message.chat.id, text=f"Не хватает средств!")

    elif "complete" in callback.data and not bool(db.ReturnValue("PCQ", "got_reward", parameter=f"WHERE player_id = {user.id} AND quest_id = {callback.data.split()[1]}")):
        quest_id = callback.data.split()[1]
        for i in NPCs_names:
            for j in quest_names:
                try:
                    if j == quest_id:
                        dt.get_reward(char, i, quest_id)
                        db.UpdateValue("PCQ", "got_reward", True, parameter=f"WHERE player_id = {user.id} AND quest_id = '{quest_id}'")
                        await bot.send_message(chat_id=callback.message.chat.id, text=f"Квест успешно завершен!")
                        if 100*(char.get_lvl()-1 + (char.get_lvl()-1)**2) <= char.get_exp():
                            char.upd_lvl(char.get_lvl()+1)
                            char.upd_sp(char.get_sp()+5)
                            await bot.send_message(chat_id=callback.message.chat.id, text=f"Уровень повышен! Доступно {char.get_sp()} очков навыков. Для прокачки перейдите в /menu")
                except:
                   pass







async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
