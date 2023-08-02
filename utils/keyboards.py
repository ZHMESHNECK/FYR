from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(*['🔎 Искать 🔍', '🛠 параметры 🛠'])

city_key = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Киев'), KeyboardButton(
                text='Одесса'), KeyboardButton(text='Львов')
        ],
        [
            KeyboardButton(text='Днепр'), KeyboardButton(
                text='Харьков'), KeyboardButton(text='Запорожье')
        ],
        [
            KeyboardButton(text='Чернигов'), KeyboardButton(
                text='Черкасы'), KeyboardButton(text='Ужгород')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

view_param = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔎 Искать 🔍')
        ],
        [
            KeyboardButton(text='🛠 параметры 🛠')
        ],
        [
            KeyboardButton(text='Изменить параметр')
        ]
    ],
    resize_keyboard=True,
)

change_board = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Город'), KeyboardButton(text='Кол. комнат')
        ],
        [
            KeyboardButton(text='Мин. цена'), KeyboardButton(text='Мин. этаж')
        ],
        [
            KeyboardButton(text='Макс. цена'), KeyboardButton(
                text='Макс. этаж')
        ],
        [
            KeyboardButton(text='Сортировка'), KeyboardButton(text='Отмена')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

price_n_key = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='3000'), KeyboardButton(text='4000')
        ],
        [
            KeyboardButton(text='5000'), KeyboardButton(text='6000')
        ],
        [
            KeyboardButton(text='7000'), KeyboardButton(text='8000')
        ],
        [
            KeyboardButton(text='Пропуск')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

price_x_key = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='6000'), KeyboardButton(text='7000')
        ],
        [
            KeyboardButton(text='8000'), KeyboardButton(text='9000')
        ],
        [
            KeyboardButton(text='10.000'), KeyboardButton(text='11.000')
        ],
        [
            KeyboardButton(text='Пропуск')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

room_key = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='1'), KeyboardButton(text='1-2')
        ],
        [
            KeyboardButton(text='2'), KeyboardButton(text='1-3')
        ],
        [
            KeyboardButton(text='3'), KeyboardButton(text='2-3')
        ],
        [
            KeyboardButton(text='Пропуск')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

floor_n_key = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='1'), KeyboardButton(text='2')
        ],
        [
            KeyboardButton(text='3'), KeyboardButton(text='4')
        ],
        [
            KeyboardButton(text='5'), KeyboardButton(text='6')
        ],
        [
            KeyboardButton(text='7'), KeyboardButton(text='8')
        ],
        [
            KeyboardButton(text='Пропуск')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

floor_x_key = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='2'), KeyboardButton(text='3')
        ],
        [
            KeyboardButton(text='4'), KeyboardButton(text='5')
        ],
        [
            KeyboardButton(text='6'), KeyboardButton(text='7')
        ],
        [
            KeyboardButton(text='8'), KeyboardButton(text='9')
        ],
        [
            KeyboardButton(text='Пропуск')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

sort_key = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Новинки')
        ],
        [
            KeyboardButton(text='Дешёвые')
        ],
        [
            KeyboardButton(text='Дорогие')
        ],
        [
            KeyboardButton(text='Пропуск')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
