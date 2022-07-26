import os
import subprocess
import random
import psutil
from datetime import date, datetime
import re
from dateutil import relativedelta

if not os.path.exists("C:\\Users\\Srinath\\Documents\\Random Episode Picker"):
    os.mkdir("C:\\Users\\Srinath\\Documents\\Random Episode Picker")

if not os.path.exists("C:\\Users\\Srinath\\Documents\\Random Episode Picker\\cache.txt"):
    open("C:\\Users\\Srinath\\Documents\\Random Episode Picker\\cache.txt", 'x')

path = "F:\\Media\\Shows\\Top Gear"
cache_path = "C:\\Users\\Srinath\\Documents\\Random Episode Picker\\cache.txt"
today = date.today()


def rand_episode(media_path=path):
    season_list = os.listdir(media_path)
    season_path = path + "\\" + random.choice(season_list)

    episode_list = os.listdir(season_path)
    episode_path = season_path + "\\" + random.choice(episode_list)
    return episode_path


def check_cache(cache=cache_path, media_path=path):
    ep = rand_episode(media_path)
    if os.path.getsize(cache) == 0:
        with open(cache, 'a') as f:
            f.write(str(today) + " - " + ep)
            f.write('\n')
        return ep
    else:
        with open(cache, 'a+') as f:
            while ep in f:
                ep = rand_episode(media_path)
            else:
                f.write(str(today) + " - " + ep)
                f.write('\n')
    return ep


def clear_cache(cache=cache_path, current_date=today):
    with open(cache, 'r+') as f:
        cache_lines = f.readlines()
        while True:
            if cache_lines:
                search_date = re.search(r'\d+-\d+-\d', cache_lines[0])
                episode_date = datetime.strptime(search_date.group(), '%Y-%m-%d').date()
                delta = relativedelta.relativedelta(current_date, episode_date)
                if delta.months >= 1:
                    cache_lines.pop(0)
                else:
                    break
            else:
                break
        if cache_lines == f.readlines():
            return
        else:
            f.seek(0)
            f.truncate()
            f.writelines(cache_lines)
            return


def open_vlc(source):
    if "vlc.exe" in (i.name() for i in psutil.process_iter()):
        os.system("TASKKILL /T /IM vlc.exe")
        subprocess.Popen(["C:/Program Files/VideoLAN/VLC/vlc.exe", source])
    else:
        subprocess.Popen(["C:/Program Files/VideoLAN/VLC/vlc.exe", source])
    return source


clear_cache()
new_episode = check_cache()
open_vlc(new_episode)
