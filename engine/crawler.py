# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=raising-bad-type
# pylint: disable=missing-final-newline

import re, os
import time, logging
from typing import Union
from collections import deque

import requests
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
from selenium import webdriver

from .utils import write_data, set_logger, dir_exist
from .model import GameCard

set_logger()
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9"}


class WebDriver:
    # Set up on google colab follows this link: https://github.com/googlecolab/colabtools/issues/3347
    @staticmethod
    def install(dir:Union[None, str]='./engine'):
        if isinstance(dir, str):
            # set path to chromedriver as per your configuration
            chromedriver_autoinstaller.install(path=dir)
        else:
            chromedriver_autoinstaller.install(cwd=True)

    @staticmethod
    def get_driver():
        # setup chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("enable-automation")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=options)
        return driver

class InstantCralwer:
    def __init__(self, install_driver=True):
        if install_driver:
            WebDriver.install(dir=None)
        self.driver = WebDriver.get_driver()
        self.BASE_URL = "https://www.instant-gaming.com/en/"
        self.crawl_queue = deque()

    def get_game_url(self, start:int=1, end:int=141):
        # game_urls = []
        for page in range(start, end):
            logging.info(msg=f"Running get_game_url at page {page}")
            # This is the trending page of instant-gaming
            URL = f"https://www.instant-gaming.com/en/search/?gametype=trending&version=2&page={page}"
            resource = requests.get(url=URL,
                        headers=headers)
            soup = BeautifulSoup(resource.content, 'html5lib')

            for a in soup.find_all('a', href=True):
                game_pattern = f"^{self.BASE_URL}+[0-9]"
                is_game_url = re.search(pattern=game_pattern, string=a['href'])
                if isinstance(is_game_url, re.Match):
        #             game_urls.append(a['href'])
                    self.crawl_queue.append(a['href'])
        logging.info(msg="Successfully processing get_game_url")
        # return game_urls

    def _get_page_content(self, url, pause=1):
        self.driver.get(url)
        # scrolling
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        html = self.driver.page_source
        bs4_obj = BeautifulSoup(html, 'html5lib')
        return bs4_obj


    def get_game_card(self, url, count:int=0, dir:str="./data/instant_gaming.txt"):
        try:
            soup = self._get_page_content(url)
            game_name = soup.find('h1', 'game-title').text
            img_url = soup.find('img', attrs={'alt': game_name,
                                            'loading': 'lazy'})['src']
            description = soup.find('span', attrs={'itemprop': 'description'}).text
            description = description.replace('\n', ' ')
            description = description.strip()

            categories = [] # Categories may contains other names that are not belong to any gaming categories due to the pattern.
            for cat in soup.find_all('a', attrs={'itemprop': 'applicationSubCategory'}):
                if not cat['content'] == 'Publishers':
                    categories.append(cat.text)

            game_card = {'name': game_name,
                        'game_url': url,
                        'description': description,
                        'img_url': img_url,
                        'categories': categories}

            game_data = GameCard.to_str(game_card)
            log_data = f"Successfully processing get_game_card at {url} - No.{count}"
            logging.info(msg=log_data, exc_info=True)
            write_data(dir=dir, content=game_data)
            return game_card
        except Exception as e:
            log_data = f'Fail to prorcess {url} - Details: {e}'
            logging.error(log_data, exc_info=True)
            return None

    def download_image(self, image_url, image_name, headers=headers, save_dir:str='./data/imgs'):
        status = True
        try:
            img_data = requests.get(url=image_url,
                                    headers=headers).content
            # image_name = '-'.join(image_name.strip().lowercase().split())
            if dir_exist(save_dir, create=True):
                image_name = image_name + ".png"
                img_dir = os.path.join(save_dir, image_name)

                with open(img_dir, 'wb') as img_handler:
                    img_handler.write(img_data)
        except:
            status = False
        return status
