import re
import requests
from bs4 import BeautifulSoup
from flask_script import Command

from app import db
from app.modules import db_models


class BeautyCrawler(Command):
    def cleanBeauty(self):
        allBeauty = db_models.Beauty.query.all()
        for i in allBeauty:
            db.session.delete(i)
        db.session.commit()

    def findAllLinks(self, soup):
        links = []
        for link in soup.findAll('div', {'class': 'title'}):
            for a in link.findAll('a'):
                links.append(a.get('href'))
        return links

    def run(self):
        self.cleanBeauty()

        res = requests.get('https://www.ptt.cc/bbs/Beauty/index.html')
        soup = BeautifulSoup(res.text, 'html.parser')
        
        prevRe = r'\/bbs\/Beauty\/index[0-9]{2,}.html'
        prev = soup.find('a', {'href': re.compile(prevRe)})

        res = requests.get('https://www.ptt.cc{}'.format(prev.get('href')))
        soup = BeautifulSoup(res.text, 'html.parser')

        links = self.findAllLinks(soup)

        for link in links:
            url = 'https://www.ptt.cc{}'.format(link)
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')

            target = r'https:.*imgur\.com\/.*'
            for a in soup.findAll('a', {'href': re.compile(target)}):
                print(a.get('href'))
                beauty = db_models.Beauty(a.get('href'))
                db.session.add(beauty)

        db.session.commit()


if __name__ == '__main__':
    crawler = BeautyCrawler()
    crawler.run()
