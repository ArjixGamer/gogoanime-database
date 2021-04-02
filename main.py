from scraper import Anime
import requests
import json
import os


link = 'https://raw.githubusercontent.com/ArjixGamer/gogoanime-random/main/all_anime.json'
ALL_ANIME = requests.get(link).json()
directory = './gogoanime'

for anime in ALL_ANIME:
    a = Anime(anime)
    data = json.loads(json.dumps({x: str(y) for x, y in a.data.items()}))
    # silly way to ensure that there are no differences between this and the saved file if it exists

    filename = f'{directory}/{a.slug}.json'

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            b = json.load(f)
            if b == data:
                continue

    if not os.path.isdir(directory):
        os.makedirs(directory)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
