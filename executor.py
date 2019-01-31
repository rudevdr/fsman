import subprocess
import shlex


queue = []
running_executor = False


def manage_executor():
    if queue and not running_executor:
        run_executor()

def run_executor():
    running_executor = True
    #create multiprocess and communicate with handler.py

def kill_executor():
    running_executor = False

def execute_command(commands):
    for command in commands:
        subprocess.Popen(shlex.split(command))

def queue(commands):
    manage_executor()
    queue.append(path)

def dequeue(path):
    queue.remove(path)
