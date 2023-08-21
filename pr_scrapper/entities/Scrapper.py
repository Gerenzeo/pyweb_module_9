import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup


class Scrapper:
    def __init__(self, url):
        self.url = url
        self.soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        self.data = []

    def grab_data(self, links):
        pass


class AuthorsScrapper(Scrapper):
    def __init__(self, url):
        super().__init__(url)
        self.soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        self.authors = []

    def grab_data(self, links):
        for link in links:
            response = requests.get(self.url + link)
            content = response.content
            soup = BeautifulSoup(content, 'html.parser')

            block = soup.find('div', class_='author-details')

            fullname = block.find('h3', class_='author-title').text
            born_date = block.find('span', class_='author-born-date').text
            born_location = block.find('span', 'author-born-location').text
            description = block.find('div', class_='author-description').text

            self.authors.append({
                "fullname": fullname,
                "born_date": born_date,
                "born_location": born_location,
                "description": str(description).strip()
            })

    def save(self):
        with open(Path(__file__).parent.parent.joinpath('data/authors.json'), 'w') as fh:
            json.dump(self.authors, fh, ensure_ascii=False, indent=4)


class QuotersScrapper(Scrapper):
    def __init__(self, url):
        super().__init__(url)
        self.soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        self.quotes = []
        self.links = []

    def grab_data(self):
        blocks = self.soup.find_all('div', attrs={"class": "quote"})
        links = []
        for block in blocks:
            quote = block.find('span', class_='text').text
            author = block.find('small', class_='author').text
            tags = [tag.text for tag in block.find('div', class_='tags').find_all('a', class_='tag')]

            links.append(block.find('a')['href'])

            self.quotes.append({
                "tags": tags,
                "author": author,
                "quote": str(quote).strip()
            })
        return links

    def save(self):
        with open(Path(__file__).parent.parent.joinpath('data/quotes.json'), 'w') as fh:
            json.dump(self.quotes, fh, ensure_ascii=False, indent=4)