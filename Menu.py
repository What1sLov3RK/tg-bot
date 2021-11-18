from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


btnSearch = KeyboardButton('/search')
btnFace = KeyboardButton('/Face')
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnFace,btnSearch)