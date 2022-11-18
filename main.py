import logging
from aiogram import Bot, Dispatcher, executor
from keyboards import *
from config import TOKEN, ADMINS
from messages import *
from admin_messages import *
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3


bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)


class WishesForm(StatesGroup):
    message = State()


class MailingForm(StatesGroup):
    mailing_text = State()


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    con = sqlite3.connect("energy_bot.db")
    cur = con.cursor()
    user = cur.execute(f"""SELECT * FROM users WHERE user_id = '{message.from_user.id}'""").fetchone()
    if user is None:
        cur.execute(f"""INSERT INTO users (user_id) VALUES ('{message.from_user.id}')""")
        con.commit()
    con.close()
    if str(message.from_user.id) in ADMINS:
        await message.answer(admin_greeting, reply_markup=admin_kb)
        await message.answer_photo(open("cat.jpg", 'rb'))
    else:
        await message.answer(greeting, reply_markup=basic_kb)


@dp.message_handler(lambda message: message.text == "Рассылка")
async def admin_mailing(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await MailingForm.mailing_text.set()
        await message.answer(mailing_inf, reply_markup=admin_cancel_kb)


@dp.message_handler(state=MailingForm.mailing_text)
async def mailing_text(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        async with state.proxy() as data:
            data['mailing_text'] = message.text
            if message.text == "Отменить":
                await state.finish()
                await message.answer("Отменено", reply_markup=admin_kb)
            else:
                await message.answer("Отправляем всем это сообщение?")
                await state.finish()
                await message.answer(message.text, reply_markup=admin_confirmation_kb)


@dp.message_handler(lambda message: message.text == "Да, мне все нравится")
async def confirmation(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        async with state.proxy() as data:
            print(data)
            con = sqlite3.connect("energy_bot.db")
            cur = con.cursor()
            cur.execute(f'''SELECT user_id FROM users''')
            mailing_base = cur.fetchall()
            con.close()
            print(mailing_base)
            # await bot.send_message(mailing_base[0][0], data['mailing_text'])
            for person in range(len(mailing_base)):
                await bot.send_message(mailing_base[person][0], data['mailing_text'])
            await message.answer('Рассылка завершена', reply_markup=admin_kb)


@dp.message_handler(lambda message: message.text == "Нет, хочу по-другому")
async def disagreement(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        await state.finish()
        await message.answer("Хорошо, ничего не отправляю", reply_markup=admin_kb)


@dp.message_handler(lambda message: message.text == "Загрузить пожелания и предложения")
async def wishes_uploading(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        con = sqlite3.connect("energy_bot.db")
        cur = con.cursor()
        cur.execute(f'''SELECT * FROM wishes_and_suggestions''')
        file = open('wishes_and_suggestions.txt', 'w+', encoding='UTF-8')
        data = cur.fetchall()
        file.write("Обратная связь\n")
        for m in data:
            file.write(m[-1] + " (" + str(m[1]) + ")" + ": " + m[2] + "\n")

        con.close()
        file.close()
        await message.reply_document(open('wishes_and_suggestions.txt', 'rb'), reply_markup=admin_kb)


@dp.message_handler(lambda message: message.text == "Узнать количество пользователей")
async def wishes_uploading(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        con = sqlite3.connect("energy_bot.db")
        cur = con.cursor()
        cur.execute(f'''SELECT COUNT(*) FROM users''')
        num = cur.fetchall()
        con.close()
        await message.answer_document(num, reply_markup=admin_kb)


@dp.message_handler(lambda message: message.text == "Энергетический клуб")
async def energy_club(message: types.Message):
    await message.answer(energy_club_description, reply_markup=[energy_clubs_kb, basic_kb])


@dp.message_handler(lambda message: message.text == "Ярмарка задач")
async def task_fair(message: types.Message):
    await message.answer(task_fair_description, reply_markup=task_fair_kb)


@dp.message_handler(lambda message: message.text == "Зарегистрировать идею")
async def sign_up_project(message: types.Message):
    await message.answer(sign_up_project_inf, reply_markup=sign_up_project_kb)


@dp.message_handler(lambda message: message.text == "Q&A")
async def q_a(message: types.Message):
    await message.answer(q_a_description, reply_markup=q_a_kb)


@dp.callback_query_handler(lambda callback: callback.data == 'common_information_energy_clubs')
async def common_inf_energy_clubs(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, common_information_energy_clubs_inf)
    await bot.send_document(callback_query.from_user.id, open('chemical_technologies.pdf', 'rb'))


@dp.callback_query_handler(lambda callback: callback.data == 'road_map')
async def road_map(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, road_map_inf, reply_markup=road_map_kb)


@dp.callback_query_handler(lambda callback: callback.data == '10_11')
async def road_map_10(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, road_map_10_11)


@dp.callback_query_handler(lambda callback: callback.data == '25_11')
async def road_map_25(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, road_map_25_11)


@dp.callback_query_handler(lambda callback: callback.data == '26_11')
async def road_map_26(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, road_map_26_11)


@dp.callback_query_handler(lambda callback: callback.data == '16_12')
async def road_map_16(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, road_map_16_12)


@dp.callback_query_handler(lambda callback: callback.data == 'active_clubs')
async def active_clubs(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, active_clubs_inf)


@dp.callback_query_handler(lambda callback: callback.data == 'successful_cases')
async def successful_cases(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, successful_cases_inf)


@dp.callback_query_handler(lambda callback: callback.data == 'how_to_participate')
async def participation(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, how_to_participate_inf)


@dp.callback_query_handler(lambda callback: callback.data == 'common_information_task_fair')
async def common_inf_task_fair(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, common_information_task_fair_inf)


@dp.callback_query_handler(lambda callback: callback.data == 'timeline')
async def timeline(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, timeline_inf)


@dp.callback_query_handler(lambda callback: callback.data == 'tracks')
async def tracks(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, tracks_inf, reply_markup=tracks_kb)


@dp.callback_query_handler(lambda callback: callback.data == 'capital_construction')
async def tracks(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, capital_construction_inf)


@dp.callback_query_handler(lambda callback: callback.data == 'esg')
async def tracks(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, esg_inf)


@dp.callback_query_handler(lambda callback: callback.data == 'new_technologies')
async def tracks(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, new_technologies_inf)


@dp.callback_query_handler(lambda callback: callback.data == 'new_materials')
async def tracks(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, new_materials_inf)


@dp.callback_query_handler(lambda callback: callback.data == 'chemical_technologies')
async def tracks(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, chemical_technologies_inf)


@dp.callback_query_handler(lambda callback: callback.data == 'possible_questions')
async def possible_questions(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, possible_questions_inf, reply_markup=possible_questions_kb)


@dp.callback_query_handler(lambda callback: callback.data == 'who_can_participate')
async def possible_questions(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, who_can_participate_inf)


@dp.callback_query_handler(lambda callback: callback.data == 'i_dont_have_team')
async def possible_questions(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, i_dont_have_team_inf)


@dp.callback_query_handler(lambda callback: callback.data == 'i_dont_have_idea')
async def possible_questions(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, i_dont_have_idea_inf)


@dp.callback_query_handler(lambda callback: callback.data == 'what_tracks')
async def possible_questions(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, what_tracks_inf)


@dp.callback_query_handler(lambda callback: callback.data == 'inappropriate_idea')
async def possible_questions(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, inappropriate_idea_inf)


@dp.callback_query_handler(lambda callback: callback.data == 'i_dont_understand_energy')
async def possible_questions(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, i_dont_understand_energy_inf)


@dp.callback_query_handler(lambda callback: callback.data == 'about_future')
async def possible_questions(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, about_future_inf)


@dp.callback_query_handler(lambda callback: callback.data == 'wishes_and_suggestions')
async def wishes_and_suggestions(callback_query: types.CallbackQuery):
    await WishesForm.message.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, wishes_and_suggestions_inf)


@dp.message_handler(state=WishesForm.message)
async def process_name(message: types.Message, state: FSMContext):
    con = sqlite3.connect("energy_bot.db")
    cur = con.cursor()
    cur.execute("""INSERT INTO wishes_and_suggestions 
    (user_id, message, user_name) values (%s, '%s', '%s')"""
                       % (message.from_user.id, message.text, message.from_user.username)).fetchall()
    con.commit()
    con.close()
    print(message.text)
    await state.finish()
    await message.answer(gratitude)


@dp.callback_query_handler(lambda callback: callback.data == 'why_is_it_for_me')
async def restart(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, why_is_it_for_me_inf)



if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
