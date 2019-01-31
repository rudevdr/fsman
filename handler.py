import subprocess
import shlex

import status
import view_output

import executor

rfile = 'running/status.json'

stdscr = view_lst = view_o = None


def init(stdscr_l, view_lst_l, view_o_l):
    global stdscr, view_lst, view_o
    stdscr = stdscr_l
    view_lst = view_lst_l
    view_o = view_o_l

def generate_commands(paths):
    commands = []
    for path in paths:
        command = "python "+path
        commands.append(command)
    return commands

def execute(path):
    #ignore already running processes
    commands = generate_commands(paths)
    executor.queue(commands)
    #view_output.update_view(view_o, command)


def kill(paths, viewo):
    pass

