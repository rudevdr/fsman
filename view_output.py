import threading
#from curses import newwin, doupdate
#from curses.panel import new_panel, update_panels
from curses import *
from curses.panel import *

import status
import sys
import os
from time import sleep

running = False
path = window = None
current_path = previous_path = None
current_read = previous_read = None


def update_view(window_object, didc_object):
    #window.erase()
    #window.box()
    global window, path
    window = window_object
    path = didc_object
    if not running:
        t = threading.Thread(target=read_display_operation)
        t.daemon = True
        t.start()
    #window.addstr(1, 1, path)

def get_path():
    return path

def read_display_operation():
    #sys.stdout.write(str("MAIN")+" ")
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
    global current_read, previous_read, current_path, previous_path
    if current_read is None:
        current_path = path
        current_read = open(path).readlines()
        previous_read = current_read
        display_operation(current_read)
        return

    current_read = open(path).readlines()
    if not previous_read == current_read:
        previous_read = current_read
        display_operation(current_read)


def display_operation(lines):
    y, x = window.getmaxyx()
    window.erase()
    init_pair(1, COLOR_BLACK, COLOR_CYAN)


    bottom_padding = 0

    if y-2+bottom_padding<= len(lines):
        lines = lines[-y+2+bottom_padding:]

    #sys.stdout.write(str(lines)+" ")
    for posy, line in enumerate(lines):
        #if posy >= len(lines):
        #    window.scroll()
        window.addstr(1+posy, 2, line)
        #window.bkgd(color_pair(1))
        window.box()
        window.refresh()

class StdoutPad:
    def __init__(self, lines, cols):
        self = curses.newpad(lines, cols)



def init(viewo_height, viewo_width, line_y, lst_window_width, keeper):
    viewo_window = newwin(viewo_height, viewo_width, line_y, lst_window_width)
    #viewo_window.scrollok(True)
    #viewo_window.idlok(True)
    viewo_panel = new_panel(viewo_window)
    viewo_window.box()
    return viewo_window
