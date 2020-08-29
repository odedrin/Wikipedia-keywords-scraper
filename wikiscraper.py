import threading
import time
import random
from datetime import datetime

class ScraperManager():
    def __init__(self, num_of_workers, rps = 50):
        self.url_gen =  None
        self.num_of_workers = 3
        self.rps = 2
        self.configurate_parameters
        self.global_semaphore = threading.Semaphore(value=self.rps)
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
            print('MANAGER: waking up 2 threads..')
            for _ in range(self.rps):
                try:
                    self.global_semaphore.release()
                except ValueError as v:
                    print('MANAGER: Cannot over-release..')

            print('MANAGER: after wakeup')

    @staticmethod
    def work(self, manager):
        current_thread = threading.current_thread()
        my_name = current_thread.name
        while True:
            print('{}: {} Waiting for work.'.format(datetime.now(), my_name))
            manager.global_semaphore.acquire()
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

manager = ScraperManager(4)
print(manager.workers)
manager.scrape()

