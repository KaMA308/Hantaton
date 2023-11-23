from json import JSONDecoder, JSONEncoder
from time import sleep

from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

with open("token.txt") as file:
    token = file.readline().strip()

bot = TeleBot(token)

main_menu_markup = (ReplyKeyboardMarkup(one_time_keyboard=True)
                    .add(KeyboardButton('Что можно сдавать?'))
                    .add(KeyboardButton('Точки сбора'))
                    .add(KeyboardButton('Рейтинг школ'))
                    .add(KeyboardButton('О проекте')))
cities: dict[str, dict[str, dict[str, str | float]]] = {}
points_data: dict[str, dict[str, str | float]] = {}

rating_text = """
Рейтинг школ можно узнать по ссылке ниже:
https://eco.blcp.ru/"""
what_to_take_text = """
Полностью со списком сдачи и требований сдачи можно ознакомиться по ссылке ниже:
https://sobiraet.yugra-ecology.ru/ecocenters"""
about_text = """
С 2022 года в ХМАО-Югре работает сеть экоцентров «Югра Собирает» - пунктов по приему вторичного сырья. Пункты открыты в Ханты-Мансийске, Нижневартовске и Сургуте.
У жителей округа появилась возможность воспитывать новые экологические привычки: сдавать на переработку пластик, стекло и макулатуру таким образом сокращать количество выбрасываемых отходов на полигон. Благодаря работе экоцентра «Югра Собирает», раздельный сбор отходов станет комфортным и привычным для горожан.
АО «Югра-Экология» — информационный куратор сети экоцентров «Югра Собирает» — пунктов по приёму вторичного сырья."""


def load_points():
    global cities, points_data
    with open("information.json") as file:
        cities = JSONDecoder().decode(file.read())
    points_data = {}
    for city in cities.values():
        for key in city.keys():
            points_data[key] = city[key]


def save_points():
    with open("information.json", "w") as file:
        file.write(JSONEncoder().encode(cities))


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
        reply_markup=main_menu_markup
    )


@bot.message_handler(func=(lambda message: message.text == "Рейтинг школ"))
def rating(message: Message):
    bot.send_message(
        message.chat.id,
        text=rating_text,
        reply_markup=main_menu_markup
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
        reply_markup=main_menu_markup
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


@bot.message_handler(func=(lambda message: message.text in points_data.keys()))
def points(message: Message):
    data: dict[str, str | float] = points_data.get(message.text)
    bot.send_message(message.chat.id, data["description"])

    bot.send_location(message.chat.id, longitude=data["longitude"], latitude=data["latitude"])


load_points()
bot.polling(non_stop=True)
