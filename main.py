from curses import *
from curses.panel import *
from glob import glob
from indicator import *

from time import sleep

#Source : https://docs.python.org/3.7/library/curses.html
#Source2: https://docs.python.org/3.7/howto/curses.html

def main(stdscr):
    curs_set(0)
    stdscr.keypad(True)

    #initilize color
    start_color()
    init_pair(1, COLOR_BLACK, COLOR_CYAN)
    init_pair(2, COLOR_BLACK, COLOR_BLUE)
    init_pair(3, COLOR_CYAN, COLOR_BLUE)

    # Clear screen
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    def notify( text, posy=height-1, posx=0):
        stdscr.clrtobot()
        stdscr.addstr(posy, posx, text, color_pair(1))
        update()

    def update():
        update_panels()
        doupdate()


    paths = glob('*')
    valid_lst_path = []
    lincs = []
    #Adds indicator
    dinc_text= "=> "
    lendinc = len(dinc_text)

    #Adds lst
    line_y = 15
    line_x = 10
    lst_width = len(max(paths, key=len))
    lst_height = len(paths)
    lst_window_height = lst_height+2
    lst_window_width = lst_width+lendinc +2
    lst_window = newwin(lst_window_height, lst_window_width, line_y , line_x)
    last_panel = new_panel(lst_window)
    lst_window.box()
    for index, path in enumerate(paths):
        lst_y = index + 1
        lst_x = lendinc + 1
        lst_window.addstr(lst_y, lst_x, path, color_pair(2)| A_REVERSE)
        valid_lst_path.append((path, line_y + lst_y, line_x + lst_x))

    dinc = Indicator(valid_lst_path, dinc_text, 0, color_pair(2) | A_REVERSE)

    def all_objects(lincs):
        lincs_obj = [inc.current_obj for inc in lincs]
        dinc_obj = dinc.current_obj
        if dinc_obj in lincs_obj:
            return lincs_obj
        else:
            return lincs_obj + [dinc_obj]

    def toggle_inc(dinc):
        index = dinc.current_index
        if index in [inc.current_index for inc in lincs]:
            inc = [inc for inc in lincs if inc.current_index == index][0]
            #inc = lincs[index]
            inc.delete_inc()
            lincs.remove(inc)
        else:
            new_inc = Indicator(valid_lst_path, dinc_text, index, color_pair(1) | A_REVERSE)
            #new_inc.move_to_bottom()
            lincs.append(new_inc)

        dinc.move_to_top()

    def update_view(vieww):
        vieww.erase()
        vieww.box()
        vieww.addstr(1, 3, ' '.join(all_objects(lincs)))


    #.Add viewo
    viewo_padding = 50
    viewo_y = line_y
    viewo_x = lst_window_width+viewo_padding
    viewo_height = 20
    viewo_width = 30
    viewo_window = newwin(viewo_height, viewo_width, viewo_y, viewo_x)
    viewo_panel = new_panel(viewo_window)
    viewo_window.box()
    viewo_window.addstr(1, 1, str(all_objects(lincs)))

    stdscr.refresh()
    update()


    while True:
        key = stdscr.getch()
        if key == ord('q'):
            stdscr.addstr(height-1, 0, "Press any key to exit", color_pair(1))
            break
        elif key == ord('j'):
            dinc.move_down()
        elif key == ord('k'):
            dinc.move_up()
        elif key == ord('n'):
            stdscr.addstr(height-1, 0, inc.current_obj, color_pair(1))
            stdscr.clrtoeol()
        elif key == ord('t'):
            toggle_inc(dinc)

        update_view(viewo_window)
        update()
        #notify(str(dinc.current_index+1)+'/' +str(len(lincs))+'/'+str([inc.current_index+1 for inc in lincs]))
        #notify(str(all_objects(lincs)))


if __name__ == '__main__':
    wrapper(main)
