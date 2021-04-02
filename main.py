from scraper import Anime
import requests
import json
import os


link = 'https://raw.githubusercontent.com/ArjixGamer/gogoanime-random/main/all_anime.json'
ALL_ANIME = requests.get(link).json()
directory = './gogoanime'

for anime in ALL_ANIME:
    a = Anime(anime)
    filename = f'{directory}/{a.slug}.json'

    if not os.path.isdir(directory):
        os.makedirs(directory)

    with open(filename, 'w') as f:
        json.dump({x: str(y) for x, y in a.data.items()}, f, indent=4)
