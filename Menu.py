from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


btnSearch = KeyboardButton('🔎')
btnFace = KeyboardButton('❤️')
btnBack = KeyboardButton('🔙')
btnShazam = KeyboardButton('Shazam!')
btnLyrics = KeyboardButton("Lyrics")
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnFace,btnSearch,btnShazam,btnLyrics)
menu2 = ReplyKeyboardMarkup(resize_keyboard = True).add(btnBack)