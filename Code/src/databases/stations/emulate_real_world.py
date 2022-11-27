from .update_stations import update_station_status
from .update_stations import random_update_availability
import threading
import time


def emulate_real_world(data) -> None:
    while True:
        random_update_availability(data)
        update_station_status(data)
        time.sleep(60)


def start_background_process(data) -> None:
    thread = threading.Thread(target=emulate_real_world, args=(data, ))
    thread.daemon = True
    thread.start()
