import threading
import psutil
from time import sleep
import os
import sys

import status
import executor


running_handler = False


def update(startup=False):
    global running_handler

    if startup:
        startup_underline()
    if not running_handler:
        run_handler()


def startup_underline():
    paths = status.get_all("paths")
    if paths:
        for path in paths:
            update_view_lst(path, underline=True)


def run_handler():
    running_handler = True

    p = threading.Thread(target=main)
    p.daemon = True
    p.start()


def main():
    #sys.stdout.write("MAIN ")
    while not status.is_empty():
        check_for_deaths()
        sleep(0.5)
    running_handler = False
    #sys.stdout.write("END ")


def check_for_deaths():
    if not status.is_empty():
       pids = status.get_all("pid")
       if pids:
           for pid in pids:
               path = status.get_from_key("path", "pid", pid)
               if path:
                   if not process_running(pid):
                       remove_stdout(path)
                       status.remove(path)
                       update_view_lst(path, underline=False)
                   else:
                       pass
                       #update view_output

def remove_stdout(path):
    filename = status.get(path, "stdout")
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass
    except TypeError:
        pass

def update_view_lst(path, underline=True):
    executor.update_view_lst(path, underline=underline)


def process_running(pid):
    try:
        p = psutil.Process(pid)
        return p.status() in [ psutil.STATUS_RUNNING, psutil.STATUS_SLEEPING ]
    except psutil.NoSuchProcess:
        return False
