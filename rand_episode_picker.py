import os
import subprocess
import random
import psutil
from datetime import date, datetime
import re
from dateutil import relativedelta
from tkinter import *
from tkinter import filedialog


docs_dir = os.path.expanduser("~\\Documents\\Random Episode Picker")
cache_path = os.path.expanduser("~\\Documents\\Random Episode Picker\\cache.txt")
dir_path = os.path.expanduser("~\\Documents\\Random Episode Picker\\directory.txt")
today = date.today()


def initialize():
    if not os.path.exists(docs_dir):
        os.mkdir(docs_dir)

    if not os.path.exists(cache_path):
        open(cache_path, 'x')

    if not os.path.exists(dir_path):
        open(dir_path, 'x')
        first_time_setup()


def first_time_setup():

    def ask_directory():
        global var
        dirname = filedialog.askdirectory()
        path_label.config(text=dirname)
        var = dirname

    def populate_directory():
        with open(dir_path, 'a+') as f:
            f.write(var)
        root.destroy()

    root = Tk()

    root.wm_title("REP - First Time Setup")

    context_label = Label(root, text="Media Folder Path: ")
    context_label.grid(row=0, column=0, padx=10)

    browse_button = Button(root, text="Browse", command=ask_directory)
    browse_button.grid(row=0, column=1)

    path_label = Label(root)
    path_label.grid(row=0, column=2, padx=5)

    save_button = Button(root, text="Save to File", command=populate_directory)
    save_button.grid(row=1, column=2)

    root.mainloop()


def dir_check():
    with open(dir_path, 'r') as f:
        return f.readline()


def rand_episode():
    season_list = os.listdir(path)
    season_path = path + "\\" + random.choice(season_list)

    episode_list = os.listdir(season_path)
    episode_path = season_path + "\\" + random.choice(episode_list)
    print(episode_path)
    return episode_path


def check_cache():
    ep = rand_episode()
    if os.path.getsize(cache_path) == 0:
        with open(cache_path, 'a') as f:
            f.write(str(today) + " - " + ep)
            f.write('\n')
        return ep
    else:
        with open(cache_path, 'a+') as f:
            while ep in f:
                ep = rand_episode()
            else:
                f.write(str(today) + " - " + ep)
                f.write('\n')
    return ep


def clear_cache():
    files_in_dir = 0
    for root_dir, cur_dir, files in os.walk(dir_path):
        files_in_dir += len(files)

    with open(cache_path, 'r+') as f:
        cache_lines = f.readlines()
        while True:
            if cache_lines:
                search_date = re.search(r'\d+-\d+-\d+', cache_lines[0])
                episode_date = datetime.strptime(search_date.group(), '%Y-%m-%d').date()
                delta = relativedelta.relativedelta(today, episode_date)
                if delta.months >= 1:
                    cache_lines.pop(0)
                elif len(cache_lines) >= files_in_dir:
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


initialize()
path = dir_check().replace('/', '\\')
clear_cache()
new_episode = check_cache()
open_vlc(new_episode)
