import os
import config as cnfg

if not os.path.exists(cnfg.MUSIC_ROOT):
    os.makedirs(cnfg.MUSIC_ROOT)

if not os.path.exists(cnfg.VOICE_ROOT):
    os.makedirs(cnfg.VOICE_ROOT)
