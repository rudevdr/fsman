import threading
from curses import newwin, doupdate
from curses.panel import new_panel, update_panels
from math import ceil

import status
import sys
import os
from time import sleep

running = False
path = window = None
current_read = previous_read = None


def update_view(window_object, didc_object):
    global window, path
    window = window_object
    path = didc_object
    if not running:
        t = threading.Thread(target=read_display_operation)
        t.daemon = True
        t.start()


def get_path():
    return path


def read_display_operation():
    #TODO: Remove ^[[K0 for clear line from printer
    running = True

    while status.exists(get_path()):
        path = get_path()
        stdout = status.get(path, "stdout")
        if os.path.exists(stdout):
            read_operation(stdout)
            pass
        sleep(0.5)

    window.erase()
    window.box()
    window.refresh()
    running = False
    #sys.stdout.write(str("END")+" ")
    #TODO: Fix multiple thread here and on handler.py


def read_operation(path):
    global current_read, previous_read

    current_read = open(path).readlines()
    if not previous_read == current_read:
        previous_read = current_read
        display_operation(current_read)


def display_operation(lines):
    valid_lines = []
    reversed_lines = reversed(lines)

    height, width = window.getmaxyx()
    height -=2
    width -=2

    window.erase()

    line_y = 0
    for line in reversed_lines:
        max_chars = height*width
        if height > 0:
            line = line[-max_chars:]
            valid_lines.insert(0, line)
            height -= ceil(len(line)/width)
        else:
            break

    for posy, line in enumerate(valid_lines):
        window.addstr(1+line_y, 2, line)
        line_y += ceil(len(line)/width)
        window.box()
        window.refresh()


def init(viewo_height, viewo_width, line_y, lst_window_width, keeper):
    viewo_window = newwin(viewo_height, viewo_width, line_y, lst_window_width)
    #viewo_window.scrollok(True)
    #viewo_window.idlok(True)
    viewo_panel = new_panel(viewo_window)
    viewo_window.box()
    return viewo_window
