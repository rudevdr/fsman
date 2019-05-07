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
from re import findall
from collections import OrderedDict
from re import split

import psutil


stdscr = view_lst = view_o = lst_data = attribute_underline  = attribute_nounderline = None

execute_queue = []
kill_queue = {}


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
    filedir = config.get("output_dir")
    if not os.path.exists(filedir):
        os.mkdir(filedir)
    filename = filedir + generate_stdout_file()
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


def kill_enqueue_old(paths):
    global kill_queue

    kill_format = config.get("kill").split()
    if len(kill_format) < 2:
        #complain() #TODO: create complain
        return
    recursive, pid = kill_format[:2]
    recursive = False if recursive == 'norecursive' else True #default is 'recursive'

    for path in paths:
        if path not in kill_queue and status.exists(path):
            pids = OrderedDict({})
            kf_pids = kill_format[1:]
            for pid in kf_pids:
                pf_pid = split('[:|-]', pid)
                pflen = len(pf_pid)
                pid, *pf_extra = pf_pid
                val_pid = status.get_from_key(pid, "paths", path)
                pf_recursive, *pf_remove = pf_extra
                val = (val_pid, True if pf_recursive == "norecursive" else False, True if pf_remove else False) if pf_extra else (val_pid, recursive, False)
                if val_pid is not None:
                    pids.update({pid: val})
            #    sys.stdout.write(f"kf_pids: {kf_pids}, kill_queue: {kill_queue}, pid: {pid}, path: {path}, val_pid: {val_pid}")
                kill_queue.update({path: pids})

    non_empty_kill_queue = {} #this queue filters empty items from kill_queue
    for k, v in kill_queue.items():
        pid, recursive, remove = v.popitem(0)[1]
        kill_process(pid, recursive)
        if any([remove, not v]):
            update_view_lst(path, underline=False)
            status.remove(k)
            continue
        non_empty_kill_queue.update({k: v})

    kill_queue = non_empty_kill_queue


def kill_enqueue(paths):
    global kill_queue

    kill_format = config.get("kill").split()
    if len(kill_format) < 2:
        #complain() #TODO: create complain
        return
    recursive, pid = kill_format[:2]
    recursive = False if recursive == 'norecursive' else True #default is 'recursive'

    for path in paths:
        if path not in kill_queue and status.exists(path):
            pids = OrderedDict({})
            kf_pids = kill_format[1:]
            for pid in kf_pids:
                val_pid = status.get_from_key(pid, "paths", path)
                if val_pid is not None:
                    pids.update({pid: val_pid})
                kill_queue.update({path: pids})

    [kill_process(v.popitem(0)[1]) for k, v in kill_queue.items() if v]
    non_empty_kill_queue = {} #this queue filters empty items from kill_queue
    for k, v in kill_queue.items():
        if not v:
            update_view_lst(path, underline=False)
            status.remove(k)
            continue
        non_empty_kill_queue.update({k: v})

    kill_queue = non_empty_kill_queue

def kill_process(pid, recursive=True):
    pid = int(pid) if type(pid) is str else pid
    try:
        proc = psutil.Process(pid)
    except psutil.NoSuchProcess:
        #complain() #TODO: complain here
        return

    if recursive:
        for child_proc in proc.children(recursive=recursive):
            sys.stdout.write(f" killing recursive: {child_proc}")
            child_proc.kill()
    proc.kill()
