from scraper import Anime, cleanse
from tqdm import tqdm
import requests
import json
import sys
import os

try:
    disable_progress_bar = True if sys.argv[1] == "pbar-off" else False
except:
    disable_progress_bar = False

link = 'https://raw.githubusercontent.com/ArjixGamer/gogoanime-random/main/all_anime.json'
ALL_ANIME = requests.get(link).json()
directory = './gogoanime'

if not disable_progress_bar:
    pbar = tqdm(total=len(ALL_ANIME), unit=' anime')


for anime in ALL_ANIME:

    if not disable_progress_bar:
        pbar.update(1)
    else:
        print('Parsing:', anime)

    a = Anime(anime)
    data = json.loads(json.dumps({x: str(y) for x, y in a.data.items()}))
    # silly way to ensure that there are no differences between this and the saved file if it exists

    filename = f'{directory}/{cleanse(a.slug)}.json'

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            b = json.load(f)
            if b == data:
                continue

    if not os.path.isdir(directory):
        os.makedirs(directory)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
