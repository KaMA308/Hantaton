from time import sleep

from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

with open("token.txt") as f:
    token = f.readline().strip()
bot = TeleBot(token)

main_menu_markup = (ReplyKeyboardMarkup(one_time_keyboard=True)
                    .add(KeyboardButton('Что можно сдавать?'))
                    .add(KeyboardButton('Точки сбора'))
                    .add(KeyboardButton('Рейтинг школ'))
                    .add(KeyboardButton('О проекте')))
cities: dict[str, dict[str, dict[str, str | float]]] = {
    "Сургут": {
        "г. Сургут УЛ. 30 ЛЕТ ПОБЕДЫ, Д. 74": {
            "latitude": 61.2574603,
            "longitude": 73.4570286,
            "description": """
ежедневно 10:00 - 20:00
обед 14:00 - 15:00
тех. перерывы
11:45 - 12:00 / 16:45 - 17:00"""
        }
    },
    "Ханты-Мансийск": {
        "УЛ. 30 ЛЕТ ПОБЕДЫ, Д. 74": {
            "latitude": 61.2574603,
            "longitude": 73.4570286,
            "description": """
ежедневно 10:00 - 20:00
обед 14:00 - 15:00
тех. перерывы
11:45 - 12:00 / 16:45 - 17:00"""
        }
    },
    "Нижневартовск": {
        "УЛ. 30 ЛЕТ ПОБЕДЫ, Д. 74": {
            "latitude": 61.2574603,
            "longitude": 73.4570286,
            "description": """
ежедневно 10:00 - 20:00
обед 14:00 - 15:00
тех. перерывы
11:45 - 12:00 / 16:45 - 17:00"""
        }
    },
}
points_data: dict[str, dict[str, str | float]] = {}


def load_points():
    for city in cities.values():
        for key in city.keys():
            points_data[key] = city[key]


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
    bot.send_message(message.chat.id, """
С 2022 года в ХМАО-Югре работает сеть экоцентров «Югра Собирает» - пунктов по приему вторичного сырья. Пункты открыты в Ханты-Мансийске, Нижневартовске и Сургуте.
У жителей округа появилась возможность воспитывать новые экологические привычки: сдавать на переработку пластик, стекло и макулатуру таким образом сокращать количество выбрасываемых отходов на полигон. Благодаря работе экоцентра «Югра Собирает», раздельный сбор отходов станет комфортным и привычным для горожан.
АО «Югра-Экология» — информационный куратор сети экоцентров «Югра Собирает» — пунктов по приёму вторичного сырья.""",
                     reply_markup=main_menu_markup)


@bot.message_handler(func=(lambda message: message.text == "Рейтинг школ"))
def rating(message: Message):
    bot.send_message(
        message.chat.id,
        "Рейтинг школ можно узнать по ссылке ниже: \n\
         https://eco.blcp.ru/",
        reply_markup=main_menu_markup
    )


@bot.message_handler(func=(lambda message: message.text == "Точки сбора"))
def places(message: Message):
    bot.send_message(message.chat.id, f"Места сбора имеются в {len(cities)} городах")
    markup = ReplyKeyboardMarkup(one_time_keyboard=True).add("обратно")
    for i in cities.keys():
        markup.add(i)
    bot.send_message(message.chat.id, "\n".join(cities.keys()), reply_markup=markup)


@bot.message_handler(func=(lambda message: message.text == "Что можно сдавать?"))
def what_to_take(message: Message):
    bot.send_message(message.chat.id,
                     "Полностью со списком сдачи и требований сдачи можно ознакомиться по ссылке ниже:\n \
                      https://sobiraet.yugra-ecology.ru/ecocenters",
                     reply_markup=main_menu_markup)


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
