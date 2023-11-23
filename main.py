from time import sleep

from telebot import types, TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

with open("token.txt") as f:
    token = f.readline().strip()
bot = TeleBot(token)


@bot.message_handler(commands=["start"])
def welcome(message: Message):
    name = message.from_user.username
    bot.send_message(message.chat.id, f"Здравствуй, {name}.")
    sleep(1)
    bot.send_message(message.chat.id, "Этот чат-бот покажет где можно утилизировать отходы в ХМАО.")
    sleep(2)
    bot.send_message(message.chat.id, "Для начало:")
    sleep(1)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    item1 = types.KeyboardButton('В Ханты-Мансийске')
    item2 = types.KeyboardButton('В Сургуте')
    item3 = types.KeyboardButton('В Нижневартовске')
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    bot.send_message(message.chat.id, "В каком городе ты живёшь?", reply_markup=markup)


@bot.message_handler(content_types=['text'], )
def trans(message: Message):
    sent = message.text
    if sent == 'В Ханты-Мансийске':
        bot.send_message(message.chat.id, "УЛ. ЧЕХОВА, Д. 74")
        bot.send_location(message.from_user.id, 61.0039543, 69.0526839)
        bot.send_message(message.chat.id, """
ежедневно 10:00 - 20:00
обед 14:00 - 15:00
тех. перерывы
11:45 - 12:00 / 16:45 - 17:00""")
        bot.send_message(message.chat.id, """
ВИДЫ СЫРЬЯ И УСЛОВИЯ ПРИЁМА:
    Коричневые, зеленые и бесцветные стеклянные бутылки и банки
1 балл / кг. от 100 грамм ПРАВИЛА ПРИЁМА:
Чистые, без крышек и ободков, бумажные этикетки можно не убирать
Необходимо сдавать по отдельности коричневое, зеленое и бесцветное стекло
Макулатура
2 балл/кг от 100грамм
ПРАВИЛА ПРИЁМА:
    Книги, газеты, журналы, бумага, гофрокартон
Чистое, сложенное в коробки или перевязанное, без жирных пятен и остатков еды, без файлов и скрепок

НЕ ПРИНИМАЕТСЯ:
    Одноразовая посуда, обои, чеки, пачки сигарет, мешки от строительных смесей, упаковка из пульперкартона, гофроупаковка от яиц


    Пластиковые ящики ПНД
5 балл/кг от 100 грамм
ПРАВИЛА ПРИЁМА:
    Чистые, без остатков еды, жира и других загрязнений
    Всех размеров, цветов и толщины""",
                         reply_markup=ReplyKeyboardMarkup(one_time_keyboard=True).
                         add(KeyboardButton('Места сбора.')).
                         add(KeyboardButton('О нас.')).
                         add(KeyboardButton('Рейтинг школ.')).
                         add(KeyboardButton('Что можно сдавать в пункты приёма?')),
                         )

    elif sent == 'В Сургуте':
        markup = (ReplyKeyboardMarkup(one_time_keyboard=True)
                  .add(KeyboardButton('Места сбора.'))
                  .add(KeyboardButton('О нас.'))
                  .add(KeyboardButton('Рейтинг школ.'))
                  .add(KeyboardButton('Что можно сдавать в пункты приёма?')))
        bot.send_message(message.chat.id, "УЛ. 30 ЛЕТ ПОБЕДЫ, Д. 74")
        bot.send_location(message.from_user.id, 61.2574603, 73.4570286)
        bot.send_message(message.chat.id, """
ежедневно 10:00 - 20:00
обед 14:00 - 15:00
тех. перерывы
11:45 - 12:00 / 16:45 - 17:00""")
        bot.send_message(message.chat.id, """
ВИДЫ СЫРЬЯ И УСЛОВИЯ ПРИЁМА:
Коричневые, зеленые и бесцветные стеклянные бутылки и банки
1 балл / кг. от 100 грамм
ПРАВИЛА ПРИЁМА:
Чистые, без крышек и ободков, бумажные этикетки можно не убирать
Необходимо сдавать по отдельности коричневое, зеленое и бесцветное стекло


Макулатура
2 балл/кг от 100грамм

ПРАВИЛА ПРИЁМА:

Книги, газеты, журналы, бумага, гофрокартон

Чистое, сложенное в коробки или перевязанное, без жирных пятен и остатков еды, без файлов и скрепок

НЕ ПРИНИМАЕТСЯ:
Одноразовая посуда, обои, чеки, пачки сигарет, мешки от строительных смесей, упаковка из пульперкартона, гофроупаковка от яиц


Пластиковые ящики ПНД
5 балл/кг от 100 грамм
ПРАВИЛА ПРИЁМА:
 
Чистые, без остатков еды, жира и других загрязнений

Всех размеров, цветов и толщины""",
                         reply_markup=markup)

    elif sent == 'В Нижневартовске':
        markup = (types.ReplyKeyboardMarkup(one_time_keyboard=True).
                  add(types.KeyboardButton('Места сбора.')).
                  add(types.KeyboardButton('О нас.')).
                  add(types.KeyboardButton('Рейтинг школ.')).
                  add(types.KeyboardButton('Что можно сдавать в пункты приёма?')))
        bot.send_message(message.chat.id, "УЛ. КОМСОМОЛЬСКОЕ ОЗЕРО, Д. 2")
        bot.send_location(message.from_user.id, 61.2574603, 73.4570286)
        bot.send_message(message.chat.id, """
ежедневно 10:00 - 20:00
обед 14:00 - 15:00
тех. перерывы
11:45 - 12:00 / 16:45 - 17:00""")
        bot.send_message(message.chat.id, """
ВИДЫ СЫРЬЯ И УСЛОВИЯ ПРИЁМА:
Коричневые, зеленые и бесцветные стеклянные бутылки и банки
 1 балл / кг. от 100 грамм
ПРАВИЛА ПРИЁМА:

Чистые, без крышек и ободков, бумажные этикетки можно не убирать

Необходимо сдавать по отдельности коричневое, зеленое и бесцветное стекло


Макулатура
 2 балл/кг от 100грамм
 ПРАВИЛА ПРИЁМА:
 
Книги, газеты, журналы, бумага, гофрокартон

Чистое, сложенное в коробки или перевязанное, без жирных пятен и остатков еды, без файлов и скрепок

НЕ ПРИНИМАЕТСЯ:
    Одноразовая посуда, обои, чеки, пачки сигарет, мешки от строительных смесей, упаковка из пульперкартона, гофроупаковка от яиц

Пластиковые ящики ПНД
 5 балл/кг от 100 грамм
  ПРАВИЛА ПРИЁМА:
  
Чистые, без остатков еды, жира и других загрязнений

Всех размеров, цветов и толщины""", reply_markup=markup)
    elif sent == "Места сбора.":
        markup = (ReplyKeyboardMarkup(one_time_keyboard=True)
                  .add(types.KeyboardButton('Места сбора.'))
                  .add(types.KeyboardButton('О нас.'))
                  .add(types.KeyboardButton('Рейтинг школ.'))
                  .add(types.KeyboardButton('Что можно сдавать в пункты приёма?')))
        bot.send_message(message.chat.id, "Места сбора имеются в трёх городах.")
        bot.send_message(message.chat.id, "В каком городе вы хотите найти точки сбора?", reply_markup=markup)

    elif sent == "О нас.":
        markup = (ReplyKeyboardMarkup(one_time_keyboard=True)
                  .add(types.KeyboardButton('Места сбора.'))
                  .add(types.KeyboardButton('О нас.'))
                  .add(types.KeyboardButton('Рейтинг школ.'))
                  .add(types.KeyboardButton('Что можно сдавать в пункты приёма?')))
        bot.send_message(message.chat.id, """
С 2022 года в ХМАО-Югре работает сеть экоцентров «Югра Собирает» - пунктов по приему вторичного сырья. Пункты открыты в Ханты-Мансийске, Нижневартовске и Сургуте.
У жителей округа появилась возможность воспитывать новые экологические привычки: сдавать на переработку пластик, стекло и макулатуру таким образом сокращать количество выбрасываемых отходов на полигон. Благодаря работе экоцентра «Югра Собирает», раздельный сбор отходов станет комфортным и привычным для горожан.
АО «Югра-Экология» — информационный куратор сети экоцентров «Югра Собирает» — пунктов по приёму вторичного сырья.""",
                         reply_markup=markup)

    elif sent == "Рейтинг школ.":
        markup = (ReplyKeyboardMarkup(one_time_keyboard=True)
                  .add(types.KeyboardButton('Места сбора.'))
                  .add(types.KeyboardButton('О нас.'))
                  .add(types.KeyboardButton('Рейтинг школ.'))
                  .add(types.KeyboardButton('Что можно сдавать в пункты приёма?')))
        bot.send_message(message.chat.id, "Рейтинг школ можно узнать по ссылке ниже: \n https://eco.blcp.ru/",
                         reply_markup=markup)

    elif sent == "Что можно сдавать в пункты приёма?":
        markup = (ReplyKeyboardMarkup(one_time_keyboard=True)
                  .add(types.KeyboardButton('Места сбора.'))
                  .add(types.KeyboardButton('О нас.'))
                  .add(types.KeyboardButton('Рейтинг школ.'))
                  .add(types.KeyboardButton('Что можно сдавать в пункты приёма?')))
        bot.send_message(message.chat.id,
                         "Полностью со списком сдачи и требований сдачи можно ознакомиться по ссылке ниже:\n https://sobiraet.yugra-ecology.ru/ecocenters",
                         reply_markup=markup)


bot.polling(non_stop=True)
