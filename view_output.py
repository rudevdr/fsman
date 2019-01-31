from curses import newwin, doupdate
from curses.panel import new_panel, update_panels

def update_view(vieww, output):
    vieww.erase()
    vieww.box()
    vieww.addstr(1, 3, output)

def init(viewo_padding, line_y, lst_window_width, keeper):

    viewo_y = line_y
    viewo_x = lst_window_width + viewo_padding
    viewo_height = 20
    viewo_width = 30
    viewo_window = newwin(viewo_height, viewo_width, viewo_y, viewo_x)
    #viewo_window.bkgd(color_pair(1))
    viewo_panel = new_panel(viewo_window)
    viewo_window.box()
    viewo_window.addstr(1, 1, str(keeper.get_all_obj()))
    return viewo_window
