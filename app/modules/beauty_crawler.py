import re
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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

    def findAllPicAndPutIntoDB(self, link):
        # import ipdb; ipdb.set_trace()
        element = self.driver.find_element_by_css_selector('a[href^="{}"]'.format(link))
        element.click()
        links = self.driver.find_elements_by_css_selector('a[href]')
        target = re.compile('https:.*imgur\.com\/.*')
        for link in links:
            href = link.get_attribute('href')
            if target.match(href):
                print(href)
                beauty = db_models.Beauty(href)
                db.session.add(beauty)
        
        self.driver.back()

    def findAllLinks(self):
        links = []
        for block in self.driver.find_elements_by_class_name('title'):
            for a in block.find_elements_by_css_selector('a[href]'):
                links.append(a.get_attribute('href').replace('https://www.ptt.cc', ''))
        return links

    def crawler(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        self.driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path='/usr/local/bin/chromedriver')
        base_url = 'https://www.ptt.cc/bbs/Beauty/index.html'
        self.driver.get(base_url)
        
        self.driver.find_element_by_xpath("//button[@value='yes']").click()
        self.driver.find_element_by_xpath("//*[contains(text(),'上頁')]").click()
        
        links = self.findAllLinks()

        for link in links:
            self.findAllPicAndPutIntoDB(link)

        self.driver.close()
#
    def run(self):
        self.cleanBeauty()
        self.crawler()
        db.session.commit()


if __name__ == '__main__':
    crawler = BeautyCrawler()
    crawler.run()
