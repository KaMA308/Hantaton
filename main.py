from json import JSONDecoder, JSONEncoder
from time import sleep

from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

with open("token.txt") as file:
    token = file.readline().strip()

bot = TeleBot(token)

owners_ids: set[int] = set()
with open("owners_ids.txt") as file:
    for line in file:
        line = line.strip()
        if len(line) != 0:
            owners_ids.add(int(line))

main_menu_markup = (ReplyKeyboardMarkup(one_time_keyboard=True)
                    .add(KeyboardButton('Что можно сдавать?'))
                    .add(KeyboardButton('Точки сбора'))
                    .add(KeyboardButton('Рейтинг школ'))
                    .add(KeyboardButton('О проекте')))

extended_markup = (ReplyKeyboardMarkup(one_time_keyboard=True)
                   .add(KeyboardButton('Что можно сдавать?'))
                   .add(KeyboardButton('Точки сбора'))
                   .add(KeyboardButton('Рейтинг школ'))
                   .add(KeyboardButton('О проекте'))
                   .add(KeyboardButton('Изменить "Что можно сдавать?"'))
                   .add(KeyboardButton('Изменить "Рейтинг школ"'))
                   .add(KeyboardButton('Изменить "О проекте"')))
cities: dict[str, dict[str, dict[str, str | float]]] = {}
points_data: dict[str, dict[str, str | float]] = {}

rating_text: str
what_to_take_text: str
about_text: str


def load_points():
    global cities, points_data, rating_text, what_to_take_text, about_text
    with open("information.json") as file:
        data = JSONDecoder().decode(file.read())
        cities = data["cities"]
        rating_text = data["rating_text"]
        what_to_take_text = data["what_to_take_text"]
        about_text = data["about_text"]
    points_data = {}
    for city in cities.values():
        for key in city.keys():
            points_data[key] = city[key]


def save_points():
    with open("information.json", "w") as file:
        file.write(JSONEncoder().encode({
            "cities": cities,
            "rating_text": rating_text,
            "what_to_take_text": what_to_take_text,
            "about_text": about_text,
        }))


@bot.message_handler(commands=["start"])
def welcome(message: Message):
    name = message.from_user.username
    bot.send_message(message.chat.id, f"Здравствуй, {name}.")
    sleep(1)
    bot.send_message(message.chat.id, "Этот чат-бот покажет где можно утилизировать отходы в ХМАО.")
    sleep(2)
    back(message)


@bot.message_handler(func=(lambda message: message.text == "О проекте"))
def about(message: Message):
    bot.send_message(
        message.chat.id,
        text=about_text,
        reply_markup=extended_markup if message.from_user.id in owners_ids else main_menu_markup
    )


@bot.message_handler(func=(lambda message: message.text == "Рейтинг школ"))
def rating(message: Message):
    bot.send_message(
        message.chat.id,
        text=rating_text,
        reply_markup=extended_markup if message.from_user.id in owners_ids else main_menu_markup
    )


@bot.message_handler(func=(lambda message: message.text == "Точки сбора"))
def places(message: Message):
    bot.send_message(message.chat.id, f"Точки сбора имеются в {len(cities)} городах")
    markup = ReplyKeyboardMarkup(one_time_keyboard=True).add("обратно")
    for i in cities.keys():
        markup.add(i)
    bot.send_message(message.chat.id, "\n".join(cities.keys()), reply_markup=markup)


@bot.message_handler(func=(lambda message: message.text == "Что можно сдавать?"))
def what_to_take(message: Message):
    bot.send_message(
        message.chat.id,
        text=what_to_take_text,
        reply_markup=extended_markup if message.from_user.id in owners_ids else main_menu_markup
    )


@bot.message_handler(func=(lambda message: message.text in cities.keys()))
def trans(message: Message):
    data: dict[str, dict[str, str | float]] = cities.get(message.text)
    bot.send_message(message.chat.id, f"В {message.text} имеется {len(data)} точек сбора")
    markup = ReplyKeyboardMarkup(one_time_keyboard=True).add("обратно")
    for i in data.keys():
        markup.add(i)
    bot.send_message(message.chat.id, "\n".join(data.keys()), reply_markup=markup)


@bot.message_handler(func=(lambda message: message.text == "обратно"))
def back(message: Message):
    bot.send_message(message.chat.id, """
Что можно узнать:
    Что можно сдавать?
    Точки сбора
    Рейтинг школ
    О проекте""", reply_markup=main_menu_markup)
    if message.from_user.id in owners_ids:
        bot.send_message(message.chat.id, """
Инструменты редактирования:
    Изменить "Что можно сдавать?"
    Изменить "Рейтинг школ"
    Изменить "О проекте" """, reply_markup=extended_markup)


edit_about_users: set[int] = set()


@bot.message_handler(
    func=(lambda message: message.text == 'Отмена' and message.from_user.id in edit_about_users))
def back_edit_about(message: Message):
    edit_about_users.remove(message.from_user.id)
    back()


@bot.message_handler(func=(lambda message: message.from_user.id in edit_about_users))
def save_about(message: Message):
    global about_text
    edit_about_users.remove(message.from_user.id)
    about_text = message.text
    save_points()
    load_points()
    bot.send_message(message.chat.id, """Текст сохранён""", reply_markup=extended_markup)


@bot.message_handler(
    func=(lambda message: message.text == 'Изменить "О проекте"' and message.from_user.id in owners_ids))
def edit_about(message: Message):
    edit_about_users.add(message.from_user.id)
    bot.send_message(message.chat.id, """
Напишите сообщение и копия его будет отправляться в разделе "О проекте"
""", reply_markup=(ReplyKeyboardMarkup(one_time_keyboard=True)
                   .add(KeyboardButton('Отмена'))))


edit_rating_users: set[int] = set()


@bot.message_handler(
    func=(lambda message: message.text == 'Отмена' and message.from_user.id in edit_rating_users))
def back_edit_rating(message: Message):
    edit_rating_users.remove(message.from_user.id)
    back()


@bot.message_handler(func=(lambda message: message.from_user.id in edit_rating_users))
def save_rating(message: Message):
    global rating_text
    edit_rating_users.remove(message.from_user.id)
    rating_text = message.text
    save_points()
    load_points()
    bot.send_message(message.chat.id, """Текст сохранён""", reply_markup=extended_markup)


@bot.message_handler(
    func=(lambda message: message.text == 'Изменить "Рейтинг школ"' and message.from_user.id in owners_ids))
def edit_rating(message: Message):
    edit_rating_users.add(message.from_user.id)
    bot.send_message(message.chat.id, """
Напишите сообщение и копия его будет отправляться в разделе "Рейтинг школ"
""", reply_markup=(ReplyKeyboardMarkup(one_time_keyboard=True)
                   .add(KeyboardButton('Отмена'))))


edit_what_users: set[int] = set()


@bot.message_handler(
    func=(lambda message: message.text == 'Отмена' and message.from_user.id in edit_what_users))
def back_edit_what(message: Message):
    edit_what_users.remove(message.from_user.id)
    back()


@bot.message_handler(func=(lambda message: message.from_user.id in edit_what_users))
def save_what(message: Message):
    global what_to_take_text
    edit_what_users.remove(message.from_user.id)
    what_to_take_text = message.text
    save_points()
    load_points()
    bot.send_message(message.chat.id, """Текст сохранён""", reply_markup=extended_markup)


@bot.message_handler(
    func=(lambda message: message.text == 'Изменить "Что можно сдавать?"' and message.from_user.id in owners_ids))
def edit_what(message: Message):
    edit_what_users.add(message.from_user.id)
    bot.send_message(message.chat.id, """
Напишите сообщение и копия его будет отправляться в разделе "Что можно сдавать?"
""", reply_markup=(ReplyKeyboardMarkup(one_time_keyboard=True)
                   .add(KeyboardButton('Отмена'))))


@bot.message_handler(func=(lambda message: message.text in points_data.keys()))
def points(message: Message):
    data: dict[str, str | float] = points_data.get(message.text)
    bot.send_message(message.chat.id, data["description"])

    bot.send_location(message.chat.id, longitude=data["longitude"], latitude=data["latitude"])


load_points()
bot.polling(non_stop=True)
