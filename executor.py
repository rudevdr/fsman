import subprocess
import shlex

import handler
import status


stdscr = view_lst = view_o = lst_data = attribute_underline  = attribute_nounderline = None

queue = []


def init(lst_data_l, attributes, stdscr_l, view_lst_l, view_o_l):
    global lst_data, attribute_underline, attribute_nounderline, stdscr, view_lst, view_o
    lst_data = lst_data_l
    attribute_underline = attributes[0]
    attribute_nounderline = attributes[1]
    stdscr = stdscr_l
    view_lst = view_lst_l
    view_o = view_o_l


def get_pos_from_path(path):
    for data in lst_data:
        if data[0] == path:
            return data


def update_view_lst(path, underline=True):
    data = get_pos_from_path(path)
    window_posy = 0
    window_posx = 0
    if underline:
        view_lst.addstr(data[1] -window_posy, data[2] - window_posx, path, attribute_underline)
    else:
        view_lst.addstr(data[1] -window_posy, data[2] - window_posx, path, attribute_nounderline)

    stdscr.refresh()
    view_lst.refresh()
    view_o.refresh()



def generate_command(path):
    command = "python "+path
    return command


def execute(path):
    command = generate_command(path)
    proc = subprocess.Popen(shlex.split(command), stdout=subprocess.DEVNULL)
    pid = proc.pid

    update_view_lst(path, underline=True)
    status.add(path, pid, command)
    dequeue([path])


def queue_updated():
    new_paths = [path for path in queue if not status.exists(path)]
    for path in new_paths:
        execute(path)
        handler.update()


def enqueue(paths):
    for path in paths:
        if path not in queue and not status.exists(path):
            queue.append(path)

    queue_updated()


def dequeue(paths):
    for path in paths:
        if path in queue:
            queue.remove(path)
