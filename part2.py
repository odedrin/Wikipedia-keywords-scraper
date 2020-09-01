import threading
import time
from urllib.request import Request, urlopen, HTTPError, URLError
from part1 import SearchEngine, Configuration
 
class ScraperManager():
    ''' 
    This class creates and manages Workers to scrape webpage at a limited rate.
    
    After initializing A ScraperManager, use scrape method.
    '''

    def __init__(self, config: Configuration):
        ''' 
        Initializing requires a Configuration instance with keys: 
        'number of workers', 'requests per second', 'url generator' and 'keywords file'. 
        '''

        self._workers = []
        self._init_workers()
        self.websearchengine = WebSearchEngine(config)
        self.ratelimiter = RateLimiter(value=config['requests per second'])

    def scrape(self):
        ''' Initiate scarping and print search results. Needs to be stopped manually '''
        for worker in self._workers:
            worker.start()
        self.ratelimiter.limit_rate()

    def _init_workers(self):
        for i in range(config['number of workers']):
            self._workers.append(Worker(target=ScraperManager.work, args=(self,), name='{}'.format(i+1)))

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
        self.ratelimiter.acquire()

class Worker(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None):
        super().__init__(target=target, name=name, daemon=True)
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

class RateLimiter(threading.BoundedSemaphore):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

    def limit_rate(self):
        time.sleep(1)
        while True:
            for _ in range(self.value):
                try:
                    self.release()
                except ValueError as v:
                    pass
            time.sleep(1)


if __name__ == '__main__':
    config = Configuration('config_file.json')
    manager = ScraperManager(config)
    manager.scrape()
