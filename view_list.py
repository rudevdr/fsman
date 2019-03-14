from indicator import *

import view_output
import keeper
import status
import executor
import handler

import sys

def update():
    update_panels()
    doupdate()

def resize_windows(stdscr, lst_window, viewo):
    pass

def init(stdscr, window_posy, window_posx, paths, inc_text):

    init_pair(1, COLOR_BLACK, COLOR_CYAN)
    init_pair(2, COLOR_BLACK, COLOR_BLUE)
    init_pair(3, COLOR_CYAN, COLOR_BLUE)
    attribute_underline = color_pair(2) + A_REVERSE + A_UNDERLINE
    attribute_nounderline = color_pair(2) + A_REVERSE


    height, width = stdscr.getmaxyx()

    lst_data = []
    lendinc = len(inc_text)

    lst_height = (11*height)//15
    lst_width = (2*width)//5
    lst_window = newwin(lst_height, lst_width, window_posy, window_posx)
    last_panel = new_panel(lst_window)
    lst_window.box()

    for index, path in enumerate(paths):
        lst_y = index + 1
        lst_x = lendinc + 1

        lst_window.addstr(lst_y, lst_x, '/'.join(path.split('/')[-2:]), attribute_nounderline)
        lst_data.append((path, window_posy + lst_y, window_posx + lst_x))

    keeper.add_didc(Indicator(lst_data, inc_text, 0, attribute_nounderline))


    viewo = view_output.init(lst_height, width-lst_width, window_posy, lst_width, keeper)

    stdscr.refresh()
    lst_window.refresh()
    viewo.refresh()

    attributes = (attribute_underline, attribute_nounderline)
    executor.init(lst_data, attributes, stdscr, lst_window, viewo)

    handler.update(startup=True)

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == KEY_RESIZE:
            height, width = stdscr.getmaxyx()
            h = (11*height)//15
            w = (2*width)//5

            lst_window.resize(h, w)
            viewo.resize(h, width - w)
            #viewo.move(window_posy, lst_width)
            #lst_window.move(window_posy, window_posx)
            sys.stdout.write(str(height)+"/"+str(width)+" ")

            stdscr.refresh()
            lst_window.refresh()
            viewo.refresh()

        elif key == ord('j'):
            keeper.move_didc_down()
        elif key == ord('k'):
            keeper.move_didc_up()
        elif key == ord('g'):
            keeper.move_didc_top()
        elif key == ord('G'):
            keeper.move_didc_bottom()
        elif key == ord('u'):
            keeper.clear_idcs()
        elif key == ord('v'):
            for index in range(0, len(lst_data)):
                keeper.enable(Indicator(lst_data, inc_text, index, color_pair(1) | A_REVERSE))
            keeper.didc_blink()
        elif key == ord('r'):
            lst_paths = [path[0] for path in lst_data]
            paths = status.get_all("paths")
            for path in paths:
                try:
                    index = lst_paths.index(path)
                    keeper.enable(Indicator(lst_data, inc_text, index, color_pair(1) | A_REVERSE))
                except ValueError:
                    pass
        elif key == ord('R'):
            lst_paths = [path[0] for path in lst_data]
            paths = status.get_all("paths")
            not_running_paths =  [path for path in lst_paths if path not in paths]
            for path in not_running_paths:
                try:
                    index = lst_paths.index(path)
                    keeper.enable(Indicator(lst_data, inc_text, index, color_pair(1) | A_REVERSE))
                except ValueError:
                    pass
        elif key == ord('S'):
            executor.execute_enqueue(keeper.get_all_obj())
        elif key == ord('K'):
            executor.kill_enqueue(keeper.get_all_obj())
        elif key == ord('t'):
            keeper.toggle_at_didc(Indicator(lst_data, inc_text, keeper.get_didc_index(), color_pair(1) | A_REVERSE))

        view_output.update_view(viewo, keeper.get_didc_obj())
        update()
        viewo.refresh()
