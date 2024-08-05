# Crawl-InstantGaming

![the crawling pipeline](./static/crawler_arch.webp)

## Introduction 

This repository, launched in 2024, intends to crawl data from [instant-gaming](https://www.instant-gaming.com/en/). 

The plain pipeline can be described as followings:


```Plain text
get_game_card() # Crawl the basic information about the game card, including: `name`, `description`, `image_url` and some of its `categories`.

download_image() # Download image of the game.

url_list = Queue([..]) # Queue of all game url that are neccessary for crawling.

while len(url_list) > 0: 
    target_url = url_list.pop()
    game_card = get_game_card(target_url)
    download_image(game_card["image_url"])

```

The more advanced pipeline includes an API that views Google Drive as cloud storage and store crawled data into that storage. To be more specific, I setup a timer that the plain pipeline would run for h-hours and rest for k-hours. During the resting time, the mentioned API would be called to do its task. 

## Usage

1. Download the repository

```bash
    git clone https://github.com/MinLee0210/Crawl-Instantgaming.git
    cd Crawl-Instantgaming
    pip install -r requirements.txt
```

2. Run the project
**NOTE:** At the moment, the project is just able to run on local machine. Excuting the app on cloud to scrape those information in real-time is a great idea for improvement.

```bash
    python main.py
```

## Suggesting projects

As an AI enthusiast, I believe the data can be used to: 

- [ ] Game Classification via Description. 
- [ ] Game Searching via Description (utilizing RAG systems).
- [ ] Search game via image (utlizing CLIP).


## Comments

+ Too relies on the basic, could use some kind of queue that utilizing the real-time scraping without pre-knowledge about the number of pages that the website has. Although it words, but it can be better.
+ Poor code.

## Reference

1. https://medium.com/kariyertech/web-crawling-general-perspective-713971e9c659
