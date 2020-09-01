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
        self.semaphore = threading.BoundedSemaphore(value=config['rps'])
        self.workers = []
        self._init_workers()
        self.websearchengine = WebSearchEngine(config)

    def scrape(self):
        for worker in self.workers:
            worker.start()
        time.sleep(1)
        while True:
            for _ in range(config['rps']):
                try:
                    self.semaphore.release()
                except ValueError as v:
                    pass
            time.sleep(1)

    def _init_workers(self):
        for i in range(config['num_of_workers']):
            self.workers.append(MyWorker(target=ScraperManager._work, args=(self,), name='{}'.format(i+1)))

    @staticmethod
    def _work(self, manager):
        current_thread = threading.current_thread()
        worker_number = current_thread.name
        while True:
            manager._request_permission_to_work()
            matches, url = manager.websearchengine.fetch_and_search()
            message = 'Worker: {}\nRandom URL: {}\nMatches: {}\n-----------------------------\n'.format(worker_number,url,matches)
            print(message)

    def _request_permission_to_work(self):
        self.semaphore.acquire()

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
        
    def fetch_and_search(self):
        text, actual_url = self._get_data(config['url_gen'])
        found = SearchEngine.search(self, text) #check what happens if url is invalid
        return found, actual_url

    def _get_data(self, url):
        try:
            request = Request(url)
            with urlopen(request) as response:
                html = response.read()
                actual_url = response.geturl()
                return str(html, encoding='utf-8'), actual_url
        except (URLError, HTTPError):
            print('Cannot open url: {}'.format(url))

if __name__ == '__main__':
    config = Configuration('config_file.json')
    manager = ScraperManager(config)
    manager.scrape()
