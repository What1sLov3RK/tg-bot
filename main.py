from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import Menu as nav
import ssl
from pytube import YouTube
import urllib.request
import urllib.parse
import re
import os


TOKEN = "1942863363:AAFfuRsNO-Ee_n--7t7Sno8NbXd3VdTWFN0"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
ssl._create_default_https_context = ssl._create_unverified_context

async def on_startup(_):
    print("Bot online!")

@dp.message_handler(commands=['start','info'])
async def command_start(message: types.Message):
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
        html_content = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + urllib.parse.quote(message.text.replace(" ", "+"),encoding="utf8"))
        search_results = re.search(r"watch\?v=(\S{11})", html_content.read().decode())
        link = "https://www.youtube.com/" + str(search_results[0])
        await bot.send_message(message.from_user.id, link)
        path = YouTube(link).streams.filter(only_audio=True).first().download(output_path=os.getcwd() + r'\music')
        mp3 = open(path, "rb")
        await bot.send_audio(message.from_user.id, mp3)

if __name__ == '__main__':
   executor.start_polling(dp,skip_updates=True,on_startup=on_startup)