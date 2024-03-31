import os
import subprocess

from engine.crawler import get_game_url, get_game_card
from engine.utils import write_df, to_csv
    

if __name__ == "__main__": 
    data_dir = './data'

    if not os.path.isdir(data_dir): 
        os.mkdir(data_dir)

    game_urls = get_game_url(start=1, end=1)

    game_cards = []

    for url in game_urls: 
        card = get_game_card(url)
        if isinstance(card, dict): 
            game_cards.append(card)

    dataset_name = 'instant_gaming.csv'
    dataset_dir = f'{data_dir}/{dataset_name}'
    # Turns crawled data into .csv 
    df = write_df(game_cards)
    to_csv(df, dir='dataset.csv')


    subprocess.run(['bash', 'commit.sh'], text=True)