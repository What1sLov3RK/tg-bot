from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import Menu as nav
import ssl
from pytube import YouTube
import urllib.request
import urllib.parse
import re
import os
from shazam import shazam

class States(Helper):
    mode = HelperMode.snake_case

    BASE = ListItem()#0
    MUSIC = ListItem()#2
    SHAZAM = ListItem()#3
    LYRICS = ListItem()#1?

TOKEN = "1942863363:AAFfuRsNO-Ee_n--7t7Sno8NbXd3VdTWFN0"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
ssl._create_default_https_context = ssl._create_unverified_context

async def on_startup(_):
    print("Bot online!")


@dp.message_handler(state='*', commands=['start','info'])
async def command_start(message: types.Message):
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    await bot.send_message(message.from_user.id , 'Hi! {0.first_name}, Im music bot!\n Use buttons below to find songs'.format(message.from_user), reply_markup=nav.mainMenu)
    await state.set_state(States.all()[0])

@dp.message_handler(state=States.MUSIC)
async def download (message: types.Message):
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    if message.text == '🔙':
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(message.from_user.id, "Ok",reply_markup=nav.mainMenu)
        await state.set_state(States.all()[0])
        return
    html_content = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + urllib.parse.quote(message.text.replace(" ", "+"),encoding="utf8"))
    search_results = re.search(r"watch\?v=(\S{11})", html_content.read().decode())
    link = "https://www.youtube.com/" + str(search_results[0])
    await bot.send_message(message.from_user.id, link)
    path = YouTube(link).streams.filter(only_audio=True).first().download(output_path=os.getcwd() + r'\music')
    with open(path, "rb") as mp3:
        await bot.send_audio(message.from_user.id, mp3)

@dp.message_handler(state=States.SHAZAM)
async def shazam(message:types.Voice):
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    if message.text == '🔙':
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(message.from_user.id, "Ok",reply_markup=nav.mainMenu)
        await state.set_state(States.all()[0])
        return
    if isinstance(message, types.Voice):
        file = await bot.get_file(message.file_id)
        file_path = file.file_path
        await bot.download_file(file_path=file_path, destination_dir=os.getcwd()+'/audio_to_shazam/', destination='shazam.ogg')
        song_name = shazam("shazam.ogg")
        await bot.send_message(message.from_user.id, song_name,reply_markup=nav.mainMenu)
    else:
        await bot.send_message(message.from_user.id, "You must send the voice message!")
    



@dp.message_handler(state=States.BASE)
async def echo_send(message: types.Message):
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    if message.text == '❤️':
        await bot.send_message(message.from_user.id,"https://www.youtube.com/watch?v=Q0EnwSTytE0")
    if message.text == '🔙':
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(message.from_user.id, "Ok",reply_markup=nav.mainMenu)
        await state.set_state(States.all()[0])
    if message.text == 'Shazam!':
        await bot.send_message(message.from_user.id,"Lets do a little Shazam!",reply_markup=nav.menu2)
        await state.set_state(States.all()[3])
    if message.text == 'Search by Lyrics':
        await bot.send_message(message.from_user.id,"Send some words from song pls",reply_markup=nav.menu2)
        await state.set_state(States.all()[1])
    if message.text == '🔎':
        await bot.send_message(message.from_user.id,"Send song name or author's name",reply_markup=nav.menu2)
        await state.set_state(States.all()[2])

@dp.message_handler(state=States.LYRICS)
async def lyrics_search(message: types.Message):
    state= dp.current_state(chat=message.chat.id, user= message.from_user.id)
    if message.text == '🔙':
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(message.from_user.id, "Ok",reply_markup=nav.mainMenu)
        await state.set_state(States.all()[0])
        return
    html_content = urllib.request.urlopen("https://search.azlyrics.com/search.php?q=" + urllib.parse.quote(message.text.replace(" ", "+"),encoding="utf8"))
    search_results =re.findall(r'https://www.azlyrics.com/lyrics/[\w\.-]+/+\w+.+html', html_content.read().decode())
    if search_results:
        name = re.search(r'https://www.azlyrics.com/lyrics/([\w.-]+)/([\w.-]+)', search_results[0])
        name=name.group(1)
        song_url = urllib.request.urlopen(search_results[0])
        song_name_url= re.search(r'<b>"+([\w.-]+)',song_url.read().decode())
        song_name=song_name_url.group(1)
        html_content = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + urllib.parse.quote(str(name+' - '+song_name).replace(" ", "+"),encoding="utf8"))
        search_results = re.search(r"watch\?v=(\S{11})", html_content.read().decode())
        link = "https://www.youtube.com/" + str(search_results[0])
        await bot.send_message(message.from_user.id, link,reply_markup=nav.mainMenu)
        path = YouTube(link).streams.filter(only_audio=True).first().download(output_path=os.getcwd() + r'\music')
        with open(path, "rb") as mp3:
            await bot.send_audio(message.from_user.id, mp3)
        await state.set_state(States.all()[0])
    else:
        await bot.send_message(message.from_user.id,"No matches, sorry😥, repeat pls")


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

if __name__ == '__main__':
   executor.start_polling(dp,skip_updates=True,on_startup=on_startup, on_shutdown=shutdown)
