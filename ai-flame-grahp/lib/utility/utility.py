import time
import pyroscope
import os
from datetime import datetime

# How much time mutex_lock() takes relative to search_radius()
MUTEX_LOCK_MULTIPLIER = 100

# How much time check_driver_availability() takes relative to search_radius()
DRIVER_AVAILABILITY_MULTIPLIER = 0.5

def mutex_lock(n):
    i = 0
    start_time = time.time()
    while time.time() - start_time < n * MUTEX_LOCK_MULTIPLIER:
        i += 1

def check_driver_availability(n):
    i = 0
    start_time = time.time()
    while time.time() - start_time < n * DRIVER_AVAILABILITY_MULTIPLIER:
        i += 1

    # Every 3 minutes this will artificially create make requests in eu-north region slow
    # this is just for demonstration purposes to show how performance impacts show up in the
    # flamegraph

    force_mutex_lock = datetime.today().minute % 3 == 0 
    if os.getenv("REGION") == "eu-north" and force_mutex_lock:
        mutex_lock(n)


def find_nearest_vehicle(n, vehicle):
    with pyroscope.tag_wrapper({ "vehicle": vehicle}):
        i = 0
        start_time = time.time()
        while time.time() - start_time < n:
            i += 1
        if vehicle == "car":
            check_driver_availability(n)
