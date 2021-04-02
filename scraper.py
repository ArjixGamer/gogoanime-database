from bs4 import BeautifulSoup
import requests
import json
import re


class AnimeType:
    def __init__(self, name, link):
        self.name = name
        self.link = link

    def __repr__(self):
        return "<Type -> {}>".format(self.name)

    def __str__(self):
        return self.name


class Genre:
    def __init__(self, name, link):
        self.name = name
        self.link = link

    def __repr__(self):
        return "<Genre -> {}>".format(self.name)

    def __str__(self):
        return self.name


class Status:
    def __init__(self, name, link):
        self.name = name
        self.link = link

    def __repr__(self):
        return "<Status -> {}>".format(self.name)

    def __str__(self):
        return self.name


class Anime:
    def __init__(self, url):
        self.link = url if 'gogoanime' in url else 'https://gogoanime.vc' + url
        self.slug = re.search(r'category/(.*)', self.link)[1]
        self.soup = BeautifulSoup(requests.get(self.link).text, 'html.parser')
        self.querySelector = self.soup.select_one
        self.querySelectorAll = self.soup.select

    @property
    def title(self):
        return self.querySelector('div.anime_info_body_bg > h1').text.strip()

    @property
    def alternative_title(self):
        return self.querySelector('div.anime_info_body_bg > p:nth-child(9)').text.replace('Other name: ', '').strip()

    @property
    def anime_type(self):
        try:
            element = self.querySelector(
                'div.anime_info_body_bg > p:nth-child(4) > a')
            return AnimeType(element.text, element['href'])
        except:
            return 'N/A'

    @property
    def description(self):
        try:
            return self.querySelector('div.anime_info_body_bg > p:nth-child(5)').text.replace('Plot Summary:', '').strip()
        except:
            return ''

    @property
    def genre(self):
        try:
            return [Genre(x['title'], x['href']) for x in self.querySelectorAll('div.anime_info_body_bg > p:nth-child(6) > a')]
        except:
            return []

    @property
    def year(self):
        try:
            return re.search(r"\d{4}", str(self.querySelector('div.anime_info_body_bg > p:nth-child(7)')))[0]
        except:
            return '6969'

    @property
    def status(self):
        try:
            element = self.querySelector(
                'div.anime_info_body_bg > p:nth-child(8) > a')
            return Status(element.text, element['href'])
        except:
            return 'N/A'

    @property
    def total_episodes(self):
        try:
            return self.querySelectorAll('ul#episode_page > li > a')[-1]['ep_end']
        except:
            return '0'

    @property
    def data(self):
        return {
            'title': self.title,
            'alternative_title': self.alternative_title,
            'slug': self.slug,
            'anime_type': self.anime_type,
            'description': self.description,
            'genre': self.genre,
            'year': self.year,
            'status': self.status,
            'total_episodes': self.total_episodes
        }

    def __repr__(self):
        return json.dumps({x: str(y) for x, y in self.data.items()}, indent=4)
