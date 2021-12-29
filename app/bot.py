from asyncio.tasks import sleep
from aiogram import Bot, types
import app.files as files
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
    BUTTON = State()

bot = Bot(token=files.cnfg.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(state='*', commands=['start','info'])
async def command_start(message: types.Message):
    await States.BASE.set()
    await bot.send_message(message.from_user.id , msg.start_new_user.format(message.from_user.first_name), reply_markup=nav.mainMenu)


@dp.message_handler(state=States.BASE)
async def echo_send(message: types.Message):
    if message.text == 'Shazam!':
        await bot.send_message(message.from_user.id, msg.starting_shazam)
        await States.SHAZAM.set()
    if message.text == 'Search by Lyrics':
        await bot.send_message(message.from_user.id, msg.lyrics_search_start)
        await States.LYRICS.set()
    if message.text == '🔎':
        await bot.send_message(message.from_user.id, msg.song_download)
        await States.MUSIC.set()


@dp.message_handler(state=States.LYRICS)
async def lyrics_search(message: types.Message):
    if message.text:
        search_results = manipulations.lyrics_search(message.text)
    if not search_results:
        await bot.send_message(message.from_user.id, msg.lyrics_search_no_matches, reply_markup=nav.backmarkup)
        return
    await bot.send_message(message.from_user.id, search_results, reply_markup=nav.downloadmarkup)
    await States.BUTTON.set()


@dp.message_handler(state=States.MUSIC)
async def download (message: types.Message):
    await bot.send_message(message.from_user.id, message.text, reply_markup=nav.downloadmarkup)
    await States.BUTTON.set()


@dp.message_handler(state=States.SHAZAM, content_types=ContentType.VOICE)
async def shazam(message:types.Voice):
    file_path = await bot.download_file_by_id(message.voice.file_id, destination_dir=files.cnfg.PATH)
    song_name = manipulations.shazam_audio(file_path.name)
    if song_name is None:
        await bot.send_message(message.from_user.id, "Song not found", reply_markup=nav.backmarkup)
        return
    await bot.send_message(message.from_user.id, song_name, reply_markup=nav.downloadmarkup)
    await States.BUTTON.set()


@dp.message_handler(state=States.SHAZAM, content_types=ContentType.TEXT)
async def shazam_menu(message:types.Message):
    await bot.send_message(message.from_user.id, msg.shazam_wrong_message_type, reply_markup=nav.backmarkup)


@dp.callback_query_handler(lambda c: c.data == 'back', state='*')
async def back (callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer(msg.back_to_main_menu, reply_markup=nav.mainMenu)
    await States.BASE.set()


@dp.callback_query_handler(lambda c: c.data == 'download', state=States.BUTTON)
async def download_audio (callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    link = manipulations.youtube_search(callback_query.message.text)
    path = manipulations.youtube_download(link)
    with open(path, "rb") as mp3:
        await callback_query.message.reply_audio(mp3, reply_markup=nav.mainMenu)

    await States.BASE.set()


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()