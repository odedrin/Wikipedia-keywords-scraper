import threading
import time
import random
from datetime import datetime
from urllib.request import Request, urlopen, HTTPError, URLError
from part1 import SearchEngine, Configuration
import json



#The following class reads the configuration file, 
class ScraperManager():
    def __init__(self, config):
        self.semaphore = threading.Semaphore(value=config.data['rps'])
        self.workers = []
        self.init_workers()
        self.websearchengine = WebSearchEngine(config)

    def init_workers(self):
        for i in range(config.data['num_of_workers']):
            self.workers.append(MyWorker(target=ScraperManager.work, args=(self,), name='{}'.format(i+1)))
        
    def scrape(self):
        for worker in self.workers:
            worker.start()
        while True:
            time.sleep(1)
            for _ in range(config.data['rps']):
                try:
                    self.semaphore.release()
                except ValueError as v:
                    print('MANAGER: Cannot over-release..')

    @staticmethod
    def work(self, manager):
        current_thread = threading.current_thread()
        worker_number = current_thread.name
        while True:
            manager.semaphore.acquire()
            matches, url = manager.websearchengine.search()
            message = '{}\nWorker: {}\nRandom URL: {}\nMatches: {}\n-----------------------------'.format(datetime.now(),worker_number,url,matches)
            print(message)

             
class MyWorker(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None):
        super().__init__(group=group, target=target, name=name)
        self.target = target
        self.args = args
        return

    def run(self):
        self.target(self.args, self.args[0])

class WebSearchEngine(SearchEngine):
    def __init__(self, config):
        SearchEngine.__init__(self, config)
        
    def search(self):
        text, actual_url = self.get_data(config.data['url_gen'])
        found = SearchEngine.search(self,text)
        return found, actual_url

    def get_data(self, url):
        try:
            request = Request(url)
            with urlopen(request) as response:
                html = response.read()
                actual_url = None
                return str(html, encoding='utf-8'), actual_url
        except (URLError, HTTPError):
            print("Cannot open url. Aborting")

if __name__ == "__main__":    
    # manager = ScraperManager()
    # manager.scrape()
    config = Configuration('config_file.json')
    manager = ScraperManager(config)
    manager.scrape()
    print(found)