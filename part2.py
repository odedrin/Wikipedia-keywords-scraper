import threading
import time
from urllib.request import Request, urlopen, HTTPError, URLError
from part1 import SearchEngine, Configuration

#The following class reads the configuration file, 
class ScraperManager():
    def __init__(self, config):
        self.semaphore = threading.BoundedSemaphore(value=config['requests per second'])
        self._workers = []
        self._init_workers()
        self.websearchengine = WebSearchEngine(config)

    def scrape(self):
        for worker in self._workers:
            worker.start()
        time.sleep(1)
        while True:
            for _ in range(config['requests per second']):
                try:
                    self.semaphore.release()
                except ValueError as v:
                    pass
            time.sleep(1)

    def _init_workers(self):
        for i in range(config['number of workers']):
            self.workers.append(MyWorker(target=ScraperManager.work, args=(self,), name='{}'.format(i+1)))

    @staticmethod
    def work(self, manager):
        current_thread = threading.current_thread()
        worker_number = current_thread.name
        while True:
            manager._request_permission_to_work()
            matches, url = manager.websearchengine.fetch_and_search()
            message = 'Worker: {}\nRandom URL: {}\nMatches: {}\n-----------------------------'.format(worker_number,url,matches)
            print(message)

    def _request_permission_to_work(self):
        self.semaphore.acquire()

class MyWorker(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None):
        super().__init__(group=group, target=target, name=name, daemon=True)
        self.target = target
        self.args = args
        return

    def run(self):
        self.target(self.args, self.args[0])

class WebSearchEngine(SearchEngine):
    def __init__(self, config):
        SearchEngine.__init__(self, config)
        
    def fetch_and_search(self):
        text, actual_url = self._fetch_data(config['url generator'])
        keywords_found = SearchEngine.search(self, text) 
        return keywords_found, actual_url

    def _fetch_data(self, url):
        try:
            with urlopen(Request(url)) as response:
                html = response.read()
                actual_url = response.geturl()
                return str(html, encoding='utf-8'), actual_url
        except (URLError, HTTPError):
            print('Cannot open url: {}. Aborting'.format(url))
            exit()

if __name__ == '__main__':
    config = Configuration('config_file.json')
    manager = ScraperManager(config)
    manager.scrape()
