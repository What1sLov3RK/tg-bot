from aiogram import Bot, types
from config import BOT_TOKEN, VOICE_ROOT
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import Menu as nav
import app.manipulations as manipulations
from app.dialogs import msg

class States(StatesGroup):
    BASE = State()
    MUSIC = State()
    SHAZAM = State()
    LYRICS = State()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(state='*', commands=['start','info'])
async def command_start(message: types.Message):
    await States.BASE.set()
    await bot.send_message(message.from_user.id , msg.start_new_user.format(message.from_user.first_name), reply_markup=nav.mainMenu)

@dp.message_handler(state=States.BASE)
async def echo_send(message: types.Message):
    if message.text == '❤️':
        await bot.send_message(message.from_user.id,"https://www.youtube.com/watch?v=Q0EnwSTytE0")
    if message.text == 'Shazam!':
        await bot.send_message(message.from_user.id, msg.starting_shazam, reply_markup=nav.menu2)
        await States.SHAZAM.set()
    if message.text == 'Search by Lyrics':
        await bot.send_message(message.from_user.id, msg.lyrics_search_start, reply_markup=nav.menu2)
        await States.LYRICS.set()
    if message.text == '🔎':
        await bot.send_message(message.from_user.id, msg.song_download,reply_markup=nav.menu2)
        await States.MUSIC.set()


@dp.message_handler(state=States.MUSIC)
async def download (message: types.Message):
    if message.text == '🔙':
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(message.from_user.id, msg.back_to_main_menu,reply_markup=nav.mainMenu)
        await States.BASE.set()
        return
    link = manipulations.youtube_search(message.text)
    await bot.send_message(message.from_user.id, link)
    path = manipulations.youtube_download(link)
    with open(path, "rb") as mp3:
        await bot.send_audio(message.from_user.id, mp3)
    

@dp.message_handler(state=States.SHAZAM, content_types=ContentType.VOICE)
async def shazam(message:types.Voice):
    file_path = await bot.download_file_by_id(message.voice.file_id, destination_dir=VOICE_ROOT)
    song_name = manipulations.shazam_audio(file_path.name)
    await bot.send_message(message.from_user.id, song_name)


@dp.message_handler(state=States.SHAZAM, content_types=ContentType.TEXT)
async def shazam_menu(message:types.Message):
    if message.text == '🔙':
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(message.from_user.id, msg.back_to_main_menu, reply_markup=nav.mainMenu)
        await States.BASE.set()
        return
    await bot.send_message(message.from_user.id, msg.shazam_wrong_message_type)


@dp.message_handler(state=States.LYRICS)
async def lyrics_search(message: types.Message):
    if message.text == '🔙':
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(message.from_user.id, msg.back_to_main_menu, reply_markup=nav.mainMenu)
        await States.BASE.set()
        return
    print(message.text)
    search_results = manipulations.lyrics_search(message.text)
    print(search_results)
    if search_results is None:
        await bot.send_message(message.from_user.id, msg.lyrics_search_no_matches)
        return
    path = manipulations.youtube_download(manipulations.youtube_search(search_results))
    with open(path, "rb") as m4a:
        await bot.send_audio(message.from_user.id, m4a)
        

async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()