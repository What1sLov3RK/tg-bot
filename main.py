from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import Menu as nav
from mp3_download import Music
import ssl


TOKEN = "1942863363:AAFfuRsNO-Ee_n--7t7Sno8NbXd3VdTWFN0"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
ssl._create_default_https_context = ssl._create_unverified_context
async def on_startup(_):
    print("Bot online!")

@dp.message_handler(commands=['start','info'])
async def command_start(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(message.from_user.id , 'Hi! {0.first_name}, Im music bot!\n Use buttons below to find songs'.format(message.from_user), reply_markup=nav.mainMenu)

@dp.message_handler(commands=['search'])
async def command_search(message: types.Message):
    await bot.delete_message(message.chat.id,message.message_id)
    await bot.send_message(message.from_user.id,"WIP",reply_markup=nav.menu2)

@dp.message_handler()
async def echo_send(message: types.Message):
    if message.text == '❤️':
        await bot.send_message(message.from_user.id,"https://www.youtube.com/watch?v=Q0EnwSTytE0")
    if message.text == '🔙':
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(message.from_user.id, "WIP",reply_markup=nav.mainMenu)
    else:
        await bot.send_message(message.from_user.id, Music().find_url_by_name(message.text))
        file_path = Music().downloader(message.text)
        mp3 = open(file_path, "rb")
        await bot.send_audio(message.from_user.id, mp3)
if __name__ == '__main__':
   executor.start_polling(dp,skip_updates=True,on_startup=on_startup)