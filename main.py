from aiogram import executor
from app import bot

if __name__ == '__main__':
   executor.start_polling(bot.dp, skip_updates=True, on_shutdown=bot.shutdown)
