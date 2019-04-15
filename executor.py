import subprocess
import shlex
import os
import sys
from time import sleep

import handler
import configurer as config
import status

from string import ascii_letters, digits
from random import randint, choices

import psutil


stdscr = view_lst = view_o = lst_data = attribute_underline  = attribute_nounderline = None

execute_queue = kill_queue = []


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
        view_lst.addstr(data[1] -window_posy, data[2] - window_posx, '/'.join(path.split('/')[-2:]), attribute_underline)
    else:
        view_lst.addstr(data[1] -window_posy, data[2] - window_posx, '/'.join(path.split('/')[-2:]), attribute_nounderline)

    stdscr.refresh()
    view_lst.refresh()
    view_o.refresh()



def generate_command(path):
    command = config.get("executor_path")+" "+path
    return command


def generate_stdout_file():
    return ''.join(choices(ascii_letters + digits + '_', k=randint(5, 20)))


def execute(path):
    command = generate_command(path)
    filename = config.get("output_dir")+generate_stdout_file()
    fileobject = open(filename, 'w', 1)

    #TODO: if program crashes show it on view output not all over file (check by running a program which crashes)
    proc = subprocess.Popen(shlex.split(command), stdout=fileobject, stderr=fileobject)
    pid = proc.pid

    update_view_lst(path, underline=True)
    status.add(path, pid, filename)
    execute_dequeue([path])


def execute_queue_updated():
    new_paths = [path for path in execute_queue if not status.exists(path)]
    for path in new_paths:
        execute(path)
        handler.update()


def execute_enqueue(paths):
    for path in paths:
        if path not in execute_queue and not status.exists(path):
            execute_queue.append(path)

    execute_queue_updated()


def execute_dequeue(paths):
    for path in paths:
        if path in execute_queue:
            execute_queue.remove(path)



def kill(path):
    if status.exists(path):
        pid = status.get_from_key("pid", "path", path)
        if handler.process_running(pid):
            kill_process(pid)

    update_view_lst(path, underline=False)
    handler.remove_stdout(path)
    status.remove(path)
    kill_dequeue([path])


def kill_process(pid, recursive=True):
    proc = psutil.Process(pid)
    if recursive:
        for child_proc in proc.children(recursive=recursive):
            child_proc.kill()

    proc.kill()


def kill_queue_updated():
    new_paths = [path for path in kill_queue if status.exists(path)]
    for path in new_paths:
        kill(path)


def kill_enqueue(paths):
    for path in paths:
        if path not in kill_queue and status.exists(path):
            kill_queue.append(path)

    kill_queue_updated()


def kill_dequeue(paths):
    for path in paths:
        if path in kill_queue:
            kill_queue.remove(path)
