from curses import *
from curses.panel import *
from curses import error as error

from time import sleep

class Indicator():

    def __init__(self, lst_data, idc_text, default_index, color_pair):
        self.idc_text = idc_text
        self.lenidc = len(self.idc_text)
        self.lst_data = lst_data

        self.color = color_pair

        start_color()
        init_pair(1, COLOR_BLACK, COLOR_CYAN)

        self.max_index = len(self.lst_data)-1
        #default
        self.default_index = default_index
        self.default_obj  = self.lst_data[self.default_index][0]
        self.default_posy = self.lst_data[self.default_index][1]
        self.default_posx = self.lst_data[self.default_index][2] - self.lenidc

        #current is default at init
        self.current_index = self.default_index
        self.current_obj   = self.default_obj
        self.current_posy  = self.default_posy
        self.current_posx  = self.default_posx

        self.idc_window_panel = self.draw_idc(self.current_posy, self.current_posx)
        self.idc_window, self.idc_panel = self.idc_window_panel[0], self.idc_window_panel[1]

    def draw_idc(self, posy, posx):
        idc_window = newwin(1, self.lenidc, posy, posx)
        idc_panel = new_panel(idc_window)
        try:
            idc_window.addstr(self.idc_text, self.color)
        except error:
            pass
        #idc_window.bkgd(color_pair(1))
        self.update_draw()
        return idc_window, idc_panel

    def increment_index(self):
        if self.current_index >= self.max_index:
            self.current_index = 0
        else:
            self.current_index +=1
        self.update_data()

    def decrement_index(self):
        if self.current_index <= 0:
            self.current_index = self.max_index
        else:
            self.current_index -=1
        self.update_data()

    def update_data(self):
        self.current_obj   = self.lst_data[self.current_index][0]
        self.current_posy  = self.lst_data[self.current_index][1]
        self.current_posx  = self.lst_data[self.current_index][2] - self.lenidc

    def move_down(self):
        self.increment_index()
        self.idc_panel.move(self.current_posy, self.current_posx)
        self.idc_panel.top()
        self.update_draw()

    def move_up(self):
        self.decrement_index()
        self.idc_panel.move(self.current_posy, self.current_posx)
        self.idc_panel.top()
        self.update_draw()

    def update_draw(self):
        update_panels()
        doupdate()

    def move_to_top(self):
        sleep(0.15)
        self.idc_panel.top()

    def move_to_bottom(self):
        sleep(0.15)
        self.idc_panel.bottom()

    def delete_inc(self):
        self.idc_window.erase()
        self.update_draw()
        del self
