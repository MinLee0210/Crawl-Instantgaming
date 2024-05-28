# Crawling https://www.instant-gaming.com/en/
import re, os
import requests, multiprocessing
import time, logging
from typing import Union
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor

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

    def install(self, dir:Union[None, str]='./engine'): 
        if isinstance(dir, str): 
            # set path to chromedriver as per your configuration
            chromedriver_autoinstaller.install(path=dir)
        else: 
            chromedriver_autoinstaller.install(cwd=True)

    def set_driver(self, options): 
        self.driver = webdriver.Chrome(options=options)

    def get_driver(self): 
        # setup chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized"); # https://stackoverflow.com/a/26283818/1689770
        options.add_argument("enable-automation"); # https://stackoverflow.com/a/43840128/1689770
        options.add_argument("--headless"); # only if you are ACTUALLY running headless
        options.add_argument("--no-sandbox"); #https://stackoverflow.com/a/50725918/1689770
        options.add_argument("--disable-dev-shm-usage"); #https://stackoverflow.com/a/50725918/1689770
        # options.add_argument("--disable-browser-side-navigation"); #https://stackoverflow.com/a/49123152/1689770
        options.add_argument("--disable-gpu"); #https://stackoverflow.com/questions/51959986/how-to-solve-selenium-chromedriver-timed-out-receiving-message-from-renderer-exc
        driver = self.set_driver(options=options)
        return driver
        
class InstantCralwer: 
    def __init__(self): 
        self.driver = WebDriver().get_driver()
        self.BASE_URL = "https://www.instant-gaming.com/en/"
        self.pool = ThreadPoolExecutor(max_workers=5)
        self.scraped_pages = set([])
        self.crawl_queue = Queue()
        
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
                    self.crawl_queue.put(a['href'])
            
        # return game_urls

    def get_page_content(self, url, pause=1): 
        self.driver.get(url)

        # scrolling
        lastHeight = self.driver.execute_script("return document.body.scrollHeight")
        #print(lastHeight)
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause)
            newHeight = self.driver.execute_script("return document.body.scrollHeight")
            if newHeight == lastHeight:
                break
            lastHeight = newHeight
            #print(lastHeight)

        html = self.driver.page_source    
        bs4_obj = BeautifulSoup(html, 'html5lib')
        return bs4_obj


    def get_game_card(self, url, count:int=0, dir:str="./data/instant_gaming.txt"):
        try:
            soup = self.get_page_content(url)
            game_name = soup.find('h1', 'game-title').text
            img_url = soup.find('img', attrs={'alt': game_name, 
                                            'loading': 'lazy'})['src']
            description = soup.find('span', attrs={'itemprop': 'description'}).text
            categories = []
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

    def download_image(self, image_url, image_name, headers=headers, save_dir:str='./data/imgs') -> bool: 
        try: 
            img_data = requests.get(url=image_url, headers=headers).content
            image_name = '-'.join(image_name.strip().lowercase().split())
            if dir_exist(save_dir, create=True): 
                image_name = image_name + ".png"
                img_dir = os.path.join(save_dir, image_name)
                with open(img_dir, 'wb') as img_handler: 
                    img_handler.write(img_data)
            log_data = f"Successfully processing download_image at {image_url}  - Save at {save_dir}"
            logging.info(msg=log_data, exc_info=True)
            return True
        except Exception as e: 
            log_data = f'Fail to prorcess {image_url} - Details: {e}'
            logging.error(log_data, exc_info=True)
            return False
        
    def run(self): 
        ...