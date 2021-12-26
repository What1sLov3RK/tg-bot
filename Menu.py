from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


btnSearch = KeyboardButton('🔎')
btnFace = KeyboardButton('❤️')
btnBack = KeyboardButton('🔙')
btnShazam = KeyboardButton('Shazam!')
btnLyrics = KeyboardButton("Search by Lyrics")
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnFace,btnSearch,btnShazam,btnLyrics)
menu2 = ReplyKeyboardMarkup(resize_keyboard = True).add(btnBack)

downloadbutton = InlineKeyboardButton('Download audio', callback_data='download')
downloadmarkup = InlineKeyboardMarkup(row_width=2).add(downloadbutton)