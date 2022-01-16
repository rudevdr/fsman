from curses import *
# from curses.panel import *
from glob import glob

import provider
import configurer as config
import subprocess

import view_list


def main(stdscr):
    curs_set(0)
    stdscr.keypad(True)

    # initilize color
    start_color()
    init_pair(1, COLOR_BLACK, COLOR_CYAN)
    init_pair(2, COLOR_BLACK, COLOR_BLUE)
    init_pair(3, COLOR_CYAN, COLOR_BLUE)

    # Clear screen
    stdscr.clear()

    paths = provider.get_paths()
    inc_text = config.get("indicator_text") + " "
    lendinc = len(inc_text)

    view_list.init(stdscr, 0, 0, paths, inc_text)

    # DON'T ADD ANYTHING HERE. AFTER CALLING VIEW_LIST's INIT, getch() will handle user input inside 'view_list' module


if __name__ == '__main__':
    wrapper(main)
