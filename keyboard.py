from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
b1=KeyboardButton("/Зарегистрироваться")
b2=KeyboardButton("/Вход")
b3=KeyboardButton('/Забыли_пароль')
b4=KeyboardButton('назад')
b5=KeyboardButton('Отправить мою геолокацию', request_location=True)
kb_client=ReplyKeyboardMarkup(one_time_keyboard=True)
kb_client.add(b1, b2).insert(b3)
kb_cl=ReplyKeyboardMarkup(one_time_keyboard=True)
nasad=ReplyKeyboardMarkup(one_time_keyboard=True)
kb_cl.add(b2)
nasad.add(b4)
kb_client_for_help=ReplyKeyboardMarkup(one_time_keyboard=True)
kb_client_for_help.add(b3, b4)
location = ReplyKeyboardMarkup(one_time_keyboard=True)
location.add(b5)