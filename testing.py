from scraper import Configuration, ScraperManager

if __name__ == "__main__":
    config = Configuration('config_file.json')
    manager = ScraperManager(config)
    manager.scrape()