from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


btnSearch = KeyboardButton('/search')
btnFace = KeyboardButton('❤️')
btnBack = KeyboardButton('🔙')
btnShazam = KeyboardButton('Shazam!')
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnFace,btnSearch,btnShazam)
menu2 = ReplyKeyboardMarkup(resize_keyboard = True).add(btnBack)