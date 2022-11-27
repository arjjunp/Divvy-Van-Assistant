import os
import threading
import json
from subprocess import call


curr_path = os.getcwd()


def create_request(task):
    request = {"origin": task.start_pluscode.replace("%2B", "+"),
               "destination": task.end_pluscode.replace("%2B", "+"),
               "travelMode": 'DRIVING'}

    with open(curr_path + '/maps/request_map.json', 'w') as fp:
        json.dump(request, fp)


def run_webpage():
    call(["python", "-m", "http.server"], cwd=curr_path + '/maps')


def create_thread():
    global thread
    thread = threading.Thread(target=run_webpage)
    thread.daemon = True
    thread.start()


def stop_thread():
    thread.daemon = "daemon thread"
