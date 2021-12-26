import os
BOT_TOKEN = "1942863363:AAFh1h41P6X-GeSLfaMXITtKeObt5-IwnIE"
API_KEY = "63a92ec98733636a55e2d2584d6cb154"
PATH = os.getcwd()
MUSIC_ROOT = os.path.join(PATH, 'music')
VOICE_ROOT = os.path.join(PATH, 'voice')

if not os.path.exists(MUSIC_ROOT):
    os.makedirs(MUSIC_ROOT)

if not os.path.exists(VOICE_ROOT):
    os.makedirs(VOICE_ROOT)