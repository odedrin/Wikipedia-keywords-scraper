# Wikipedia-keywords-scraper
This API enables scanning a website using a random URL generator, looking for a list of keyword at a limited requests rate. 
the specific configuration file in the repo uses the Wikipedia random url generator but any other website encoded with 'utf-8' can be scraped using the API.

Features
--------
- Search for a list of keywords in a string.
- Search for a list of keywords in a website.
- Case insensitivity in the search. Find keywords regardless of hyphens or missing space between words (For example, if a required keyword is 'Star wars', 
the scraper will detect: 'starwars', 'StAr-WarS', 'STARWARS!!!'. The scraper will not detect: 'Star warss')

Installation
------------
The program requires Python 3 and nothing else. The API uses only the built-in Python 3 libraries.

Manual
--------
In order to use the API, first edit config_file.json with the following parameters:
- 'number of workers': the number of worker (threads) that will be created and run.
- 'requests per second': the maximum requests per second (RPS) rate. Can be a larger or smaller number than the number of workers.
- 'url generator': a valid link that generates random urls. If a regular link is given, the same webpage will be scraped over and over again.
- 'keywords file': a text file containing a list of keywords to be searched.

#### WARNING - In order to avoid overloading a server, make sure the RPS isn't too high.

After setting up the parameters, create a Configuration instance, then create a ScraperManager instance. In order to begin scraping, simply use the ScraperManager's 
scrape method. The program will continue running until stopped manually!

Contribute:
------------
- Source code: https://github.com/odedrin/Wikipedia-keywords-scraper

Support:
-------
For more information contact odedrin@gmail.com
