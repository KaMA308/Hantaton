from json import JSONDecoder, JSONEncoder
from time import sleep

import requests
from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

with open("token.txt") as file:
    token = file.readline().strip()

bot = TeleBot(token)

owners_ids: set[str] = set()
with open("owners_names.txt") as file:
    for line in file:
        line = line.strip()
        if len(line) != 0:
            owners_ids.add(line)

main_menu_markup = (ReplyKeyboardMarkup(one_time_keyboard=True)
                    .add(KeyboardButton('Что можно сдавать?'))
                    .add(KeyboardButton('Точки сбора'))
                    .add(KeyboardButton('Найди ближайшею точку'))
                    .add(KeyboardButton('Рейтинг школ'))
                    .add(KeyboardButton('О проекте')))

extended_markup = (ReplyKeyboardMarkup(one_time_keyboard=True)
                   .add(KeyboardButton('Что можно сдавать?'))
                   .add(KeyboardButton('Точки сбора'))
                   .add(KeyboardButton('Рейтинг школ'))
                   .add(KeyboardButton('О проекте'))
                   .add(KeyboardButton('Добавить место сбора'))
                   .add(KeyboardButton('Изменить вступительный текст"'))
                   .add(KeyboardButton('Изменить "О проекте"'))
                   .add(KeyboardButton('Изменить "Что можно сдавать?"'))
                   .add(KeyboardButton('Изменить "Рейтинг школ"'))
                   )
cities: dict[str, dict[str, dict[str, str | float]]] = {}
points_data: dict[str, dict[str, str | float]] = {}

rating_text: str
what_to_take_text: str
about_text: str
welcome_text: str


def load_points():
    global cities, points_data, rating_text, what_to_take_text, about_text, welcome_text
    with open("information.json") as file:
        data = JSONDecoder().decode(file.read())
        cities = data["cities"]
        rating_text = data["rating_text"]
        what_to_take_text = data["what_to_take_text"]
        about_text = data["about_text"]
        welcome_text = data["welcome_text"]
    points_data = {}
    for city in cities.values():
        for key in city.keys():
            points_data[key] = city[key]


def save_points():
    with open("information.json", "w") as file:
        file.write(JSONEncoder(ensure_ascii=False, indent=2).encode({
            "cities": cities,
            "rating_text": rating_text,
            "what_to_take_text": what_to_take_text,
            "about_text": about_text,
            "welcome_text": welcome_text,
        }))


@bot.message_handler(func=(lambda message: message.from_user.id in edit_about_users))
def save_about(message: Message):
    global about_text
    edit_about_users.remove(message.from_user.id)
    about_text = message.text
    save_points()
    load_points()
    bot.send_message(message.chat.id, """Текст сохранён""", reply_markup=extended_markup)


@bot.message_handler(func=(lambda message: message.from_user.id in edit_rating_users))
def save_rating(message: Message):
    global rating_text
    edit_rating_users.remove(message.from_user.id)
    rating_text = message.text
    save_points()
    load_points()
    bot.send_message(message.chat.id, """Текст сохранён""", reply_markup=extended_markup)


@bot.message_handler(func=(lambda message: message.from_user.id in edit_what_users))
def save_what(message: Message):
    global what_to_take_text
    edit_what_users.remove(message.from_user.id)
    what_to_take_text = message.text
    save_points()
    load_points()
    bot.send_message(message.chat.id, """Текст сохранён""", reply_markup=extended_markup)


@bot.message_handler(func=(lambda message: message.from_user.id in edit_welcome_users))
def save_welcome(message: Message):
    global welcome_text
    edit_welcome_users.remove(message.from_user.id)
    welcome_text = message.text
    save_points()
    load_points()
    bot.send_message(message.chat.id, """Текст сохранён. Что бы увидеть вступление напишите /start""",
                     reply_markup=extended_markup)


@bot.message_handler(commands=["start"])
def welcome(message: Message):
    name = message.from_user.username
    bot.send_message(message.chat.id, "Здравствуй, {name}.")
    sleep(1)
    bot.send_message(message.chat.id, welcome_text)
    sleep(2)
    back(message)


@bot.message_handler(func=(lambda message: message.text == "О проекте"))
def about(message: Message):
    bot.send_message(
        message.chat.id,
        text=about_text,
        reply_markup=extended_markup if message.from_user.username in owners_ids else main_menu_markup
    )


@bot.message_handler(func=(lambda message: message.text == "Рейтинг школ"))
def rating(message: Message):
    data = JSONDecoder().decode(
        requests.get("https://api.eco.blcp.ru/api/router/getcount?territory=&type_of_institution=0&unit_type=1").text)
    text = ""
    for i in data[0:10:]:
        text += i["school"] + "\n " + str(i["groups"]["Итого"]) + " балов\n"
    bot.send_message(
        message.chat.id,
        text=text,
    )
    bot.send_message(
        message.chat.id,
        text=rating_text,
        reply_markup=extended_markup if message.from_user.username in owners_ids else main_menu_markup
    )


@bot.message_handler(func=(lambda message: message.text == "Что можно сдавать?"))
def what_to_take(message: Message):
    bot.send_message(
        message.chat.id,
        text=what_to_take_text,
        reply_markup=extended_markup if message.from_user.username in owners_ids else main_menu_markup
    )


@bot.message_handler(func=(lambda message: message.text == 'Найди ближайшею точку'))
def find_first(message: Message):
    bot.send_message(
        message.chat.id,
        text="Отошлите геопизицию средствами телеграмма и вам будет показана ближайшая точка",
        reply_markup=extended_markup if message.from_user.username in owners_ids else main_menu_markup
    )


class Point:
    def __init__(self):
        self.city: str | None = None
        self.address: str | None = None
        self.latitude: float | None = None
        self.longitude: float | None = None
        self.description: str | None = None


add_point: dict[int, Point] = {}


@bot.message_handler(
    func=(lambda message: message.text == 'Добавить место сбора' and message.from_user.username in owners_ids))
def add_points(message: Message):
    add_point[message.from_user.id] = Point()
    bot.send_message(
        message.chat.id,
        "Введите название города где находится место сбора",
        reply_markup=(
            ReplyKeyboardMarkup(one_time_keyboard=True)
            .add(KeyboardButton('Отмена'))
        )
    )


@bot.message_handler(
    func=(lambda message: message.from_user.id in add_point.keys() and add_point[message.from_user.id].city is None))
def save_point_city(message: Message):
    add_point[message.from_user.id].city = message.text
    bot.send_message(
        message.chat.id,
        "Введите адрес где находится место сбора (Город тоже должен быть в адресе)",
        reply_markup=(
            ReplyKeyboardMarkup(one_time_keyboard=True)
            .add(KeyboardButton('Отмена'))
        )
    )


@bot.message_handler(
    func=(lambda message: message.from_user.id in add_point.keys() and add_point[message.from_user.id].address is None))
def save_point_address(message: Message):
    add_point[message.from_user.id].address = message.text
    bot.send_message(
        message.chat.id,
        'Укажите геопозицию места сбора (Нажмите на скрепку в правом нижнем углу. Дальше снизу будет "location")',
        reply_markup=(
            ReplyKeyboardMarkup(one_time_keyboard=True)
            .add(KeyboardButton('Отмена'))
        )
    )


@bot.message_handler(
    content_types=['location'],
    func=(
            lambda message: message.from_user.id in add_point.keys() and add_point[
                message.from_user.id].longitude is None))
def save_point_location(message: Message):
    add_point[message.from_user.id].longitude = message.location.longitude
    add_point[message.from_user.id].latitude = message.location.latitude
    bot.send_message(
        message.chat.id,
        'Напишите описание места сбора. Копия написанного текста будет выводится при выводе данных о месте сбора',
        reply_markup=(
            ReplyKeyboardMarkup(one_time_keyboard=True)
            .add(KeyboardButton('Отмена'))
        )
    )


@bot.message_handler(content_types=['location'])
def save_point_location(message: Message):
    mi = 1000000000
    longitude = message.location.longitude
    latitude = message.location.latitude
    mi_key = ""
    for f, i in points_data.items():
        if mi > (i["longitude"] - longitude) ** 2 + (i["latitude"] - latitude) ** 2:
            mi = (i["longitude"] - longitude) ** 2 + (i["latitude"] - latitude) ** 2
            mi_key = f
    bot.send_message(message.chat.id, mi_key)
    message.text = mi_key
    points(message)


@bot.message_handler(
    func=(lambda message: message.from_user.id in add_point.keys()))
def save_point_location(message: Message):
    add_point[message.from_user.id].description = message.text
    point = add_point[message.from_user.id]
    add_point.pop(message.from_user.id)
    if point.city not in cities.keys():
        cities[point.city] = {}

    cities[point.city][point.address] = {
        "longitude": point.longitude,
        "latitude": point.latitude,
        "description": point.description,
    }
    save_points()
    load_points()
    bot.send_message(
        message.chat.id,
        'Данные сохранены',
        reply_markup=extended_markup
    )


@bot.message_handler(func=(lambda message: message.text == "Точки сбора"))
def places(message: Message):
    if len(cities) == 1:
        bot.send_message(message.chat.id, "\n".join(cities.keys()))
        message.text = next(iter(cities.keys()))
        trans(message)
        return
    bot.send_message(message.chat.id, f"Точки сбора имеются в {len(cities)} городах")
    markup = ReplyKeyboardMarkup(one_time_keyboard=True).add("обратно")
    for i in cities.keys():
        markup.add(i)
    bot.send_message(message.chat.id, "\n".join(cities.keys()), reply_markup=markup)


@bot.message_handler(func=(lambda message: message.text in cities.keys()))
def trans(message: Message):
    data: dict[str, dict[str, str | float]] = cities.get(message.text)
    if len(data) == 1:
        bot.send_message(message.chat.id, "\n".join(data.keys()))
        message.text = next(iter(data.keys()))
        points(message)
        return
    bot.send_message(message.chat.id, f"В городе {message.text} имеется {len(data)} точек сбора")
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
    Найди ближайшею точку
    Рейтинг школ
    О проекте""", reply_markup=main_menu_markup)
    if message.from_user.username in owners_ids:
        bot.send_message(message.chat.id, """
Инструменты редактирования:
    Добавить место сбора
    Изменить вступительный текст"
    Изменить "О проекте"
    Изменить "Что можно сдавать?"
    Изменить "Рейтинг школ" """, reply_markup=extended_markup)


edit_about_users: set[int] = set()
edit_rating_users: set[int] = set()
edit_what_users: set[int] = set()
edit_welcome_users: set[int] = set()


@bot.message_handler(
    func=(lambda message: message.text == 'Отмена' and (
            message.from_user.id in edit_about_users) or
                          message.from_user.id in edit_what_users or
                          message.from_user.id in edit_rating_users or
                          message.from_user.id in edit_welcome_users or
                          message.from_user.id in add_point.keys()))
def back_edit_about(message: Message):
    if message.from_user.id in edit_about_users:
        edit_about_users.remove(message.from_user.id)
    elif message.from_user.id in edit_what_users:
        edit_what_users.remove(message.from_user.id)
    elif message.from_user.id in edit_rating_users:
        edit_rating_users.remove(message.from_user.id)
    elif message.from_user.id in edit_welcome_users:
        edit_welcome_users.remove(message.from_user.id)
    back(message)


@bot.message_handler(
    func=(lambda message: message.text == 'Изменить "О проекте"' and message.from_user.username in owners_ids))
def edit_about(message: Message):
    edit_about_users.add(message.from_user.id)
    bot.send_message(message.chat.id, """
Напишите сообщение и копия его будет отправляться в разделе "О проекте"
""", reply_markup=(ReplyKeyboardMarkup(one_time_keyboard=True)
                   .add(KeyboardButton('Отмена'))))


@bot.message_handler(
    func=(lambda message: message.text == 'Изменить "Рейтинг школ"' and message.from_user.username in owners_ids))
def edit_rating(message: Message):
    edit_rating_users.add(message.from_user.id)
    bot.send_message(message.chat.id, """
Напишите сообщение и копия его будет отправляться в разделе "Рейтинг школ"
""", reply_markup=(ReplyKeyboardMarkup(one_time_keyboard=True)
                   .add(KeyboardButton('Отмена'))))


@bot.message_handler(
    func=(lambda message: message.text == 'Изменить "Что можно сдавать?"' and message.from_user.username in owners_ids))
def edit_what(message: Message):
    edit_what_users.add(message.from_user.id)
    bot.send_message(message.chat.id, """
Напишите сообщение и копия его будет отправляться в разделе "Что можно сдавать?"
""", reply_markup=(ReplyKeyboardMarkup(one_time_keyboard=True)
                   .add(KeyboardButton('Отмена'))))


@bot.message_handler(
    func=(lambda message: message.text == 'Изменить вступительный текст' and message.from_user.username in owners_ids))
def edit_welcome(message: Message):
    edit_welcome_users.add(message.from_user.id)
    bot.send_message(message.chat.id, """
Напишите сообщение и копия его будет отправляться в вступлении
""", reply_markup=(ReplyKeyboardMarkup(one_time_keyboard=True)
                   .add(KeyboardButton('Отмена'))))


@bot.message_handler(func=(lambda message: message.text in points_data.keys()))
def points(message: Message):
    data: dict[str, str | float] = points_data.get(message.text)
    bot.send_message(message.chat.id, data["description"])

    bot.send_location(message.chat.id, longitude=data["longitude"], latitude=data["latitude"])


load_points()
bot.polling(non_stop=True)
