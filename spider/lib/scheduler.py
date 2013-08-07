import os
import redis as Redis
from rq import Connection, Queue, Worker, use_connection
from rq_scheduler import Scheduler
from datetime import datetime

import tencentspider as spider

class SpiderScheduler:

    # INIT with an instance of spider
    def __init__(self, spider):
        
        # redis_url = os.getenv('REDISTOGO_URL', 'http://localhost:6379')
        MITRAS_REDIS_HOST = os.getenv('MITRAS_REDIS_HOST', "127.0.0.1")
        MITRAS_REDIS_PORT = os.getenv('MITRAS_REDIS_PORT', 6379)
        self.MITRAS_REDIS_NAMESPACE = os.getenv('MITRAS_REDIS_NAMESPACE', "redis")
        redis = Redis.Redis(MITRAS_REDIS_HOST)

        # Scheduler
        q = Queue('test',connection=redis)
        use_connection()
        self.scheduler = Scheduler() # Get a scheduler for the "default" queue

        # Get spider instance
        self.spider =spider


    def schedule(self):
        # self.refresh_tokens()
        pass 

    def run(self):
        # exec rqscheduler
        pass


    def refresh_tokens(self):
        self.scheduler.schedule(
            scheduled_time=datetime.now(), # Time for first execution
            func=self.spider.create_token(),    # Function to be queued
            interval=60,                   # Time before the function is called again in s
            repeat=None                     # Repeat this number of times (None=forever)
        )
        return

    def extract_tweets(self):
        self.scheduler.schedule(
            scheduled_time=datetime.now(), # Time for first execution
            func=self.spider.create_token(),    # Function to be queued
            interval=60,                   # Time before the function is called again in s
            repeat=None                     # Repeat this number of times (None=forever)
        )
        pass

        