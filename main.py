__author__= "OctoOpt"
__version__ = "0.0.0"

# ================================
import time, os, asyncio

from engine.crawler import InstantCralwer
from engine.g_drive import GoogleDriveService
from engine.utils import yaml_read, set_logger, write_data
import logging
# ================================

set_logger()

config = yaml_read(filename="./configs/config.yaml")
crawler = InstantCralwer(install_driver=True)
service = GoogleDriveService(credential_dir=config["google_credential_dir"])


async def upload_ggdrive():
    service.upload_data(content_dir=os.path.join(config["data_dir"], config["dataset_name"]),
                        google_drive_id=config["google_drive_data_id"],
                        mimetype="text/txt",
                        rename=True)

    img_dir = os.path.join(config["data_dir"], "imgs")
    for image in os.listdir(img_dir):
        content_dir = os.path.join(img_dir, image)
        service.upload_data(content_dir=content_dir,
                            google_drive_id=config["google_drive_image_id"],
                            mimetype="image/jpeg")

async def crawler_run(rest=True):
    count = 0
    while True:
        try:
            start = time.time()
            target_url = crawler.crawl_queue.pop()
            game_card = crawler.get_game_card(url=target_url,
                                            count=count)
            downloaded_image_status = crawler.download_image(image_url=game_card["img_url"],
                                                    image_name=game_card["name"])
            
            if not downloaded_image_status: 
                lost_msg =f"Get error while downloading image {game_card}"
                logging.error(lost_msg)
                write_data(dir='./log/lost.txt', content=lost_msg)
            if rest:
                end = time.time()
                if end - start >= 2 * 60 * 60:
                    await asyncio.sleep(60 * 15) # Rest for 60 secs * 15

            if len(crawler.crawl_queue) == 0: # The crawl_queue is empty
                msg = "Crawl queue is empty, done the process"
                logging.error(msg=msg)
                raise msg
                
        except Exception as e: # There are problems during the process
            logging.error(msg=f"Fail to run crawler - Details: {e}")
            continue

async def pipeline():
    crawler.get_game_url()
    # print(crawler.crawl_queue)
    await asyncio.gather(crawler_run(),
                         upload_ggdrive())
                         

# ================================
if __name__ == "__main__":
    logo = """
==================================================    START THE PROCESS    ======================================================
'     ___                         _    _____              _                  _                                    _
'    / __\ _ __   __ _ __      __| |   \_   \ _ __   ___ | |_   __ _  _ __  | |_          __ _   __ _  _ __ ___  (_) _ __    __ _
'   / /   | '__| / _` |\ \ /\ / /| |    / /\/| '_ \ / __|| __| / _` || '_ \ | __| _____  / _` | / _` || '_ ` _ \ | || '_ \  / _` |
'  / /___ | |   | (_| | \ V  V / | | /\/ /_  | | | |\__ \| |_ | (_| || | | || |_ |_____|| (_| || (_| || | | | | || || | | || (_| |
'  \____/ |_|    \__,_|  \_/\_/  |_| \____/  |_| |_||___/ \__| \__,_||_| |_| \__|        \__, | \__,_||_| |_| |_||_||_| |_| \__, |
'                                                                                        |___/                              |___/
=================================================================================================================================
"""
    print(logo)
    print('Press Ctrl+C to exit')

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.run(pipeline())
    except (KeyboardInterrupt, SystemExit):
        pass 
