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


class Genre:
    def __init__(self, name, link):
        self.name = name
        self.link = link

    def __repr__(self):
        return "<Genre -> {}>".format(self.name)


class Status:
    def __init__(self, name, link):
        self.name = name
        self.link = link

    def __repr__(self):
        return "<Status -> {}>".format(self.name)


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
        element = self.querySelector(
            'div.anime_info_body_bg > p:nth-child(4) > a')
        return AnimeType(element.text, element['href'])

    @property
    def description(self):
        return self.querySelector('div.anime_info_body_bg > p:nth-child(5)').text.replace('Plot Summary:', '').strip()

    @property
    def genre(self):
        return [Genre(x['title'], x['href']) for x in self.querySelectorAll('div.anime_info_body_bg > p:nth-child(6) > a')]

    @property
    def year(self):
        return re.search(r"\d{4}", str(self.querySelector('div.anime_info_body_bg > p:nth-child(7)')))[0]

    @property
    def status(self):
        element = self.querySelector(
            'div.anime_info_body_bg > p:nth-child(8) > a')
        return Status(element.text, element['href'])

    @property
    def total_episodes(self):
        try:
            return self.querySelectorAll('ul#episode_page > li > a')[-1]['ep_end']
        except:
            return '0'

    @property
    def data(self):
        return {
            'Title': self.title,
            'OtherTitle': self.alternative_title,
            'Slug': self.slug,
            'Type': self.anime_type,
            'Description': self.description,
            'Genre': self.genre,
            'Year': self.year,
            'Status': self.status,
            'TotalEpisodes': self.total_episodes
        }

    def __repr__(self):
        return json.dumps({x: str(y) for x, y in self.data.items()}, indent=4)
