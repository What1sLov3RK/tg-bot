import os
BOT_TOKEN = "1942863363:AAFh1h41P6X-GeSLfaMXITtKeObt5-IwnIE"
API_KEY = "d7cf75af52de7e0b9c6ae5b2751a42be"
PATH = os.getcwd()
MUSIC_ROOT = os.path.join(PATH, 'music')
VOICE_ROOT = os.path.join(PATH, 'voice')

if not os.path.exists(MUSIC_ROOT):
    os.makedirs(MUSIC_ROOT)

if not os.path.exists(VOICE_ROOT):
    os.makedirs(VOICE_ROOT)