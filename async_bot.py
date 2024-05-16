import asyncio
import json
import locations
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.media_group import InputMedia
import datas as dt
import DataBase as DB
from locations import *
import keyboards as kb
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
        db.fill("users", user.id, user.username, "Неизвестный игрок", 1, 0, 100, 100, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0,
                True, None, None, None, None, None, None, None, None, None, None, None, None, None, "nick", None, None,
                None, None, None)
        db.fill("inv", user.id, 1, 1)
        db.fill("PAQ", '',user.id)
        db.fill("PCQ", '', user.id, '')
    else:
        await message.answer("Дважды начать не получится!", keyboard = None)


@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    await message.answer_photo(FSInputFile('images/menu.png'), reply_markup=kb.set_menu)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@dp.message(Command("photo"))
async def send_photo(message: types.Message):
    await message.answer_photo(FSInputFile('images/start_loc.png'))

@dp.message()
async def message_handler(message: types.Message):
    msg = message.text
    user = message.from_user
    char = DB.Character("users", user.id)
    # a = await user.get_profile_photos()
    # print(a.photos[0][1].file_id)



    # Отправляем карусель медиафайлов в ответ на сообщение
    await message.answer(text="негры", reply_markup=InlineKeyboardMarkup(row_width=1,inline_keyboard=[[InlineKeyboardButton(text="карусель",callback_data='crs')]]))
    action = char.get_action()

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
            await message.answer("Огры известны как яростные берсерки. Уверены в этом выборе?",
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
                                       reply_markup=keyboard_location("Уэльгард", location))

        else:
            await message.answer(f"Правильно, лучше посмотреть всё!", reply_markup=kb.race_keyboard)
            char.upd_action("racing")

    elif action in list(loc_name for loc_name in location):
        flag = 1
        if msg in list(loc_name for loc_name in location):
            await loc(msg, message)
            char.upd_action(msg)

        elif msg in list(NPC_name for NPC_name in dt.NPCs):
            for loc_name in location:
                if flag:
                    for NPC_name in location[loc_name]["NPCs"]:
                        if msg == NPC_name and action == loc_name and flag:
                            for i in dt.NPCs[NPC_name]["quests"]:
                                RC = dt.NPCs[NPC_name]["quests"][i]["required_completed"]
                                db.cur.execute(f"SELECT * FROM PAQ WHERE player_id = {user.id}")
                                PCQ = list(i[0] for i in db.cur.fetchall())
                                db.cur.execute(f"SELECT * FROM PAQ WHERE player_id = {user.id}")
                                PAQ = list(i[0] for i in db.cur.fetchall())
                                if not(dt.NPCs[NPC_name]["action"] is None):
                                    if dt.NPCs[NPC_name]["action"] == "tractir":
                                        pass


                                if flag:
                                    if RC == [] and not (i in PAQ):
                                        await message.answer(f"{msg}:\n\n{dt.NPCs[msg]['phrase']}", reply_markup=kb.quest_button(i))
                                        break

                                    else:
                                        for j in RC:
                                            if (j not in PCQ and j not in PAQ or j == "") and flag:
                                                pass
                                            else:
                                                flag = 0
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
            await loc(char.get_action(), message)



@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    user = callback.from_user
    char = DB.Character("users", user.id)
    if callback.data == "closed":
        id = user.id
        await callback.answer('Вы закрыли меню.', show_alert=True)
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)

    if callback.data == "char":
        await bot.edit_message_media(types.InputMediaPhoto(media='images/menu.png'), chat_id=callback.message.chat.id,
                                     message_id=callback.message.message_id, reply_markup=kb.char_menu)

    if callback.data == "bag":
        await callback.answer('Ваша сумка пуста.', show_alert=True)

    if callback.data == "skills":
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
        await bot.edit_message_media(types.InputMediaPhoto(media='images/menu.png'), chat_id=callback.message.chat.id,
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

    if callback.data == "crs":
        media = types.
        media.attach_photo(types.InputFile('images/menu.png'), 'Превосходная фотография')
        media.attach_photo(types.InputFile('images/profguild.png'), 'Превосходная фотография 2')
        await bot.send_media_group(callback.message.chat.id, media=media)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
