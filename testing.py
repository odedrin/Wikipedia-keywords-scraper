import threading
import time
from datetime import datetime

rps = 2

global_semaphore = threading.Semaphore(value=rps)

class Scraper():
    def __init__(self):
        self.workers = []

    def init_workers(self, num_of_workers):
        for i in range(num_of_workers):
            self.workers.append(threading.Thread(target=Scraper.work, args=(self,), name=('Thread{}'.format(i+1))))

    def run_workers(self):
        for worker in self.workers:
            worker.start()

    @staticmethod
    def work(self):
        current_thread = threading.current_thread()
        my_name = current_thread.name
        while True:
            print('{}: {} Waiting for work.'.format(datetime.now(), my_name))
            global_semaphore.acquire()
            print('{}: {} Scraping...'.format(datetime.now(), my_name))
            time.sleep(5)

s = Scraper()
s.init_workers(5)
s.run_workers()

while True:
    time.sleep(1)
    print('MAIN: waking up 2 threads..')
    for _ in range(rps):
        try:
            global_semaphore.release()
        except ValueError as v:
            print('MAIN: Cannot over-release..')

    print('MAIN: after wakeup')