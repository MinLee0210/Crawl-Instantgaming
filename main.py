__author__= "OctoOpt"
__version__ = "0.0.0"


import asyncio
from datetime import datetime, date

from engine.crawler import get_game_url, get_game_card, download_image
from engine.utils import yaml_read, set_logger
import logging

config = yaml_read(filename="./configs/config.yaml")
set_logger()


def crawling():
    try:
        # Start
        logging.info("Started crawling {}...". format(datetime.now()))

        # Crawl its trending games
        game_urls = get_game_url(start=config["pages"][0], 
                                end=config["pages"][1])

        count = 0 
        for url in game_urls: 
            card = get_game_card(url, 
                                count=count)
            image = download_image(image_url=card["image_url"], 
                                   image_name=card["name"])
            count += 1
        # End
        logging.info("Finished crawling {}...".format(datetime.now()))
    except Exception as e: 
        logging.error(e)

if __name__ == "__main__": 
    logo = """
'     ___                         _    _____              _                  _                                    _               
'    / __\ _ __   __ _ __      __| |   \_   \ _ __   ___ | |_   __ _  _ __  | |_          __ _   __ _  _ __ ___  (_) _ __    __ _ 
'   / /   | '__| / _` |\ \ /\ / /| |    / /\/| '_ \ / __|| __| / _` || '_ \ | __| _____  / _` | / _` || '_ ` _ \ | || '_ \  / _` |
'  / /___ | |   | (_| | \ V  V / | | /\/ /_  | | | |\__ \| |_ | (_| || | | || |_ |_____|| (_| || (_| || | | | | || || | | || (_| |
'  \____/ |_|    \__,_|  \_/\_/  |_| \____/  |_| |_||___/ \__| \__,_||_| |_| \__|        \__, | \__,_||_| |_| |_||_||_| |_| \__, |
'                                                                                        |___/                              |___/ 
"""
    print("********** START THE PROCESS **********")
    print(logo)
    print("***************************************")
    crawling()

    print('Press Ctrl+C to exit')

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass 