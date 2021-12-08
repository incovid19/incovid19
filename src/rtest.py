# test_scheduler.py

from redis import Redis

from rq import Queue

from rq_scheduler import Scheduler

from datetime import datetime

#from my_module import wrapper

from datetime import timedelta

from rmain import rscheduler



scheduler = Scheduler(connection=Redis()) # Get a scheduler for the "default" queue

job = scheduler.schedule(scheduled_time=datetime.utcnow(), func=rscheduler, repeat=None, interval=14400)

print("Enqueued job ",job)
