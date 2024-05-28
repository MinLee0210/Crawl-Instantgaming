import os

from pydantic import BaseModel

class GameCard(BaseModel): 
    name: str
    game_url: str
    description: str
    img_url: str
    categories: list[str]

    @staticmethod
    def to_str(content:dict) -> str: 
        game_card = GameCard(**content)
        categories = ','.join(game_card.categories)
        result = "::".join([game_card.name, game_card.game_url, game_card.description, 
                            game_card.img_url, categories])
        return result
    
class LocalGameData(BaseModel): 
    data_dir: str
    image_dir: str