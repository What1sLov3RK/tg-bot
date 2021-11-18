from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


btnSearch = KeyboardButton('/search')
btnFace = KeyboardButton('❤️')
btnBack = KeyboardButton('🔙')
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnFace,btnSearch)
menu2 = ReplyKeyboardMarkup(resize_keyboard = True).add(btnBack)