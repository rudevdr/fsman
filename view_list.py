from indicator import *

import view_output
import keeper

def update():
    update_panels()
    doupdate()

def init(stdscr, window_posy, window_posx, paths, inc_text):

    init_pair(1, COLOR_BLACK, COLOR_CYAN)
    init_pair(2, COLOR_BLACK, COLOR_BLUE)
    init_pair(3, COLOR_CYAN, COLOR_BLUE)


    lst_data = []
    lendinc = len(inc_text)

    lst_width = len(max(paths, key=len))
    lst_height = len(paths)
    lst_window_height = lst_height + 2
    lst_window_width = lst_width + lendinc + 2
    lst_window = newwin(lst_window_height, lst_window_width, window_posy, window_posx)
    last_panel = new_panel(lst_window)
    lst_window.box()
    for index, path in enumerate(paths):
        lst_y = index + 1
        lst_x = lendinc + 1
        lst_window.addstr(lst_y, lst_x, path, color_pair(2) | A_REVERSE)
        lst_data.append((path, window_posy + lst_y, window_posx + lst_x))

    keeper.add_didc(Indicator(lst_data, inc_text, 0, color_pair(2) | A_REVERSE))

    view_output_padding = 50
    viewo = view_output.init(20, window_posy, lst_window_width, keeper)

    stdscr.refresh()
    lst_window.refresh()
    viewo.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('j'):
            keeper.move_didc_down()
        elif key == ord('k'):
            keeper.move_didc_up()
        elif key == ord('n'):
            stdscr.addstr(height - 1, 0, inc.current_obj, color_pair(1))
            stdscr.clrtoeol()
        elif key == ord('t'):
            keeper.toggle_idc(Indicator(lst_data, inc_text, keeper.get_didc_index(), color_pair(1) | A_REVERSE))

        view_output.update_view(viewo, keeper)
        update()
        viewo.refresh()
