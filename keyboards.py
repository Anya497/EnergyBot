from aiogram import types


basic_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
basic_kb.add("Энергетический клуб", "Ярмарка задач").add("Зарегистрировать идею", "Q&A")

energy_clubs_kb = types.InlineKeyboardMarkup()
energy_clubs_kb.add(types.InlineKeyboardButton(text="Дорожная карта", callback_data="road_map")) \
    .add(types.InlineKeyboardButton(text="Действующие клубы", callback_data="active_clubs")) \
    .add(types.InlineKeyboardButton(text="Успешные кейсы", callback_data="successful_cases")) \
    .add(types.InlineKeyboardButton(text="Как стать участником?", callback_data="how_to_participate"))

task_fair_kb = types.InlineKeyboardMarkup()
task_fair_kb.add(types.InlineKeyboardButton(text="А что еще меня ждет?", callback_data="common_information_task_fair"))\
    .add(types.InlineKeyboardButton(text="Таймлайн", callback_data="timeline")) \
    .add(types.InlineKeyboardButton(text="Треки", callback_data="tracks")) \
    .add(types.InlineKeyboardButton(text="Подключиться к трансляции", url="https://www.google.com/"))

sign_up_project_kb = types.InlineKeyboardMarkup()
sign_up_project_kb.add(types.InlineKeyboardButton(text="Регистрация проекта", url="https://docs.google.com/forms/d/e/"
                                                                                  "1FAIpQLScnXul-UruvP3zqdLcfP6r-Gm3cf"
                                                                                  "c1xYZ5uJ12ZD9y0iq0HPQ/viewform"))\
    .add(types.InlineKeyboardButton(text="Поиск команды", url="https://docs.google.com/forms/d/e/1FAIpQLScGNNUw7ik19_q"
                                                              "7BAA8wiRAuNOMs9BiEL2uashnYYDQbTswJA/viewform"))

q_a_kb = types.InlineKeyboardMarkup()
q_a_kb.add(types.InlineKeyboardButton(text="Ответы на возможные вопросы", callback_data="possible_questions"))\
    .add(types.InlineKeyboardButton(text="Предложения и пожелания", callback_data="wishes_and_suggestions")) \
    .add(types.InlineKeyboardButton(text="Почему это для меня?", callback_data="why_is_it_for_me")) \
    .add(types.InlineKeyboardButton(text="Чат поддержки", url="https://t.me/puuuush_29"))


admin_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_kb.add("Рассылка", "Загрузить пожелания и предложения")\
    .add("Энергетический клуб", "Ярмарка задач")\
    .add("Зарегистрировать идею", "Q&A")

admin_cancel_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_cancel_kb.add("Отменить")

admin_confirmation_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_confirmation_kb.add("Да, мне все нравится").add("Нет, хочу по-другому")

road_map_kb = types.InlineKeyboardMarkup()
road_map_kb.add(types.InlineKeyboardButton(text="10.11 - \"Ярмарка задач\"", callback_data="10_11"))\
    .add(types.InlineKeyboardButton(text="25.11 - \"Питч-баттл\"", callback_data="25_11")) \
    .add(types.InlineKeyboardButton(text="26.11 - 15.12 - \"Стартап-лаборатория\"", callback_data="26_11")) \
    .add(types.InlineKeyboardButton(text="16.12 - \"Состязание стартапов\"", callback_data="16_12"))

tracks_kb = types.InlineKeyboardMarkup()
tracks_kb.add(types.InlineKeyboardButton(text="Капитальное строительство", callback_data="capital_construction"))\
    .add(types.InlineKeyboardButton(text="Энергопереход и ESG-повестка", callback_data="esg")) \
    .add(types.InlineKeyboardButton(text="Новые производственные технологии", callback_data="new_technologies")) \
    .add(types.InlineKeyboardButton(text="Новые материалы и технологии нанесения покрытий", callback_data="new_materials"))\
    .add(types.InlineKeyboardButton(text="Химические технологии", callback_data="chemical_technologies"))

possible_questions_kb = types.InlineKeyboardMarkup()
possible_questions_kb.add(types.InlineKeyboardButton(text="1", callback_data="who_can_participate"),
                          types.InlineKeyboardButton(text="2", callback_data="i_dont_have_team"),
                          types.InlineKeyboardButton(text="3", callback_data="i_dont_have_idea"))\
    .add(types.InlineKeyboardButton(text="4", callback_data="what_tracks"),
         types.InlineKeyboardButton(text="5", callback_data="inappropriate_idea"),
         types.InlineKeyboardButton(text="6", callback_data="i_dont_understand_energy")) \
    .add(types.InlineKeyboardButton(text="7", callback_data="about_future"))




