# Crawl-InstantGaming

![the crawling pipeline](./static/crawler_arch.webp)

## Introduction 

This repository, launched in 2024, intends to crawl data from [instant-gaming](https://www.instant-gaming.com/en/). 

The process is simple, it can be done in 4 steps: 

1. It scrapes the basic information about the game card, including: `name`, `description`, `image_url` and some of its `categories`.
2. It download the images that are crawled from previous steps.
3. Clean the categories. 
4. Run step 1 till all games are crawled.

## Usage

1. Download the repository

```
    git clone https://github.com/MinLee0210/Crawl-Instantgaming.git
    cd Crawl-Instantgaming
    pip install -r requirements.txt
```

2. Run the project
**NOTE:** At the moment, the project is just able to run on local machine. Excuting the app on cloud to scrape those information in real-time is a great idea for improvement.

```
    python main.py
```

## Suggesting projects

- [ ] Game Classification via Description. 
- [ ] Game Searching via Description (utilizing RAG systems).
- [ ] Search game via image (utlizing CLIP).


## Comments

+ Too relies on the basic, could use some kind of queue that utilizing the real-time scraping without pre-knowledge about the number of pages that the website has. Although it words, but it can be better.
+ Still can not be executed automatically.
+ Poor code.

<!-- ## Reference

1. https://medium.com/kariyertech/web-crawling-general-perspective-713971e9c659
2. https://medium.com/kariyertech/web-crawling-general-perspective-713971e9c659  -->