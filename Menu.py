from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


btnSearch = KeyboardButton('🔎')
btnFace = KeyboardButton('❤️')
btnShazam = KeyboardButton('Shazam!')
btnLyrics = KeyboardButton("Search by Lyrics")
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnFace,btnSearch,btnShazam,btnLyrics)


downloadbutton = InlineKeyboardButton('Download audio', callback_data='download')
backbutton = InlineKeyboardButton('Back', callback_data='back')
downloadmarkup = InlineKeyboardMarkup(row_width=2).add(downloadbutton, backbutton)
backmarkup = InlineKeyboardMarkup(row_width=2).add(backbutton)