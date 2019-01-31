import json

SFILE = 'running/status.json'


def write(status):
    with open(SFILE, 'w') as f:
        json.dump(status, f, indent=4)


def clear():
    write({})
    return {}


def read():
    try:
        with open(SFILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}
    except FileNotFoundError:
        clear()


def add(path, pid, command):
    status = read()

    status.update({path: {"pid": pid, "command": command}})

    write(status)


def exists(path):
    status = read()

    return path in status


def remove(path):
    '''
    returns success of removing of the item, True if remove successful else False
    '''
    path = str(path)
    if exists(path):
        status = read()
        status.pop(path)
        write(status)
        return True
    else:
        return False


def valid_key(key):
    if key in ["path", "paths", "PATH", "Paths", "pa"]:
        return "paths"
    elif key in ["pid", "PID", "Pid", "p", "pi"]:
        return "pid"
    elif key in ["command", "COMMAND", "Command", "c"]:
        return "command"
    else:
        return None


def get(path, key):
    '''
    returns value of key for a path. returns None if invalid key or path
    '''

    path = str(path)
    key = valid_key(key)
    if key not in ["pid", "command"]:
        return None

    if exists(path):
        status = read()
        return status.get(path).get(key)
    else:
        return None


def get_all(key):
    status = read()
    paths = list(status.keys())
    key = valid_key(key)

    if key == "paths":
        return paths
    elif key in ["pid", "command"]:
        values = []
        for path in paths:
            value = get(path, key)
            values.append(value)
        return values
    else:
        return None


def read_list():
    status = read()

    status_list = []
    for k, v in status.items():
        v_items = list(v.values())
        status_list.append([k]+v_items)

    return status_list
