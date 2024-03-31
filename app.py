from engine import get_game_url, get_game_card
from engine import write_df, to_csv
    
    

if __name__ == "__main__": 
    game_urls = get_game_url(start=1, 
                             end=141)

    game_cards = []

    for url in game_urls: 
        card = get_game_card(url)
        if isinstance(card, dict): 
            game_cards.append(card)

        # Turns crawled data into .csv 
        df = write_df(game_cards)
        to_csv(df, dir='dataset.csv')