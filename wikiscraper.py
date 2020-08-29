import threading
import time
import random
from datetime import datetime
from urllib.request import Request, urlopen, HTTPError, URLError

#The following class reads the configuration file, 
class ScraperManager():
    def __init__(self, rps = 3):
        self.url_gen =  None
        self.num_of_workers = 8
        self.rps = rps
        self.configurate_parameters("")
        self.semaphore = threading.Semaphore(value=self.rps)
        self.workers = []
        self.init_workers()

    def configurate_parameters(self, file):
        pass #read configuration file, set url_gen, num_of_workers and rps according to the config file.

    def init_workers(self):
        for i in range(self.num_of_workers):
            self.workers.append(MyWorker(target=ScraperManager.work, args=(self,)))
        
    def scrape(self):
        for worker in self.workers:
            worker.start()
        while True:
            time.sleep(1)
            print('MANAGER: waking up {} threads..'.format(self.rps))
            for _ in range(self.rps):
                try:
                    self.semaphore.release()
                except ValueError as v:
                    print('MANAGER: Cannot over-release..')

            print('MANAGER: after wakeup')

    @staticmethod
    def work(self, manager):
        current_thread = threading.current_thread()
        my_name = current_thread.name
        while True:
            print('{}: {} Waiting for work.'.format(datetime.now(), my_name))
            manager.semaphore.acquire()
            print('{}: {} Scraping...'.format(datetime.now(), my_name))
            time.sleep(5)
             
class MyWorker(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None):
        super().__init__(group=group, target=target, name=name)
        self.target = target
        self.args = args
        return

    def run(self):
        self.target(self.args, self.args[0])


def request(url):
    try:
        request = Request(url)
        response = urlopen(request)
        html = response.read()
        response.close()
    except (HTTPError, URLError):
        print ("Failed to get article")
    print(html[:100])
    
get_data('http://en.wikipedia.org/wiki/Special:Random')
# manager = ScraperManager()
# manager.scrape()

