# Testing the Crawler
from engine.crawler import InstantCralwer

crawler = InstantCralwer()
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9"}

game_card = crawler.get_game_card(url='https://www.instant-gaming.com/en/15920-buy-balatro-pc-game-steam/')
print(game_card)
done = crawler.download_image(image_url=game_card['img_url'],
                                image_name=game_card['name'])
print(done)
